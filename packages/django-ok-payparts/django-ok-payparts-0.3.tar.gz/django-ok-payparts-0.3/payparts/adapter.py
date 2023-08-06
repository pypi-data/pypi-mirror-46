import json
from base64 import b64encode
from hashlib import sha1
from typing import Dict

from django.utils.translation import ugettext_lazy as _

from payparts.client import PayPartsAPIClient
from payparts.exceptions import InvalidAuthDataError
from payparts.models import Log
from payparts.settings import (
    API_PASSWORD,
    API_STORE_ID,
    API_REDIRECT_URL
)
from payparts.templates import prepare_order, prepare_log

__all__ = (
    'PayPartsAdapter',
)


class PayPartsAdapter:
    api_client_class = PayPartsAPIClient

    def __init__(
            self,
            parts_count: int = 2,
            merchant_type: str = 'PP',
            response_url: str = None,
            redirect_url: str = None
    ):
        self.password: str = API_PASSWORD
        self.store_id: str = API_STORE_ID
        if not self.password:
            raise InvalidAuthDataError(
                code='password',
                message=_('You must provide a password.')
            )
        if not self.password or not self.store_id:
            raise InvalidAuthDataError(
                code='store_id',
                message=_('You must provide a store id.')
            )

        self.api_client = self.api_client_class()
        self.parts_count: int = parts_count
        self.merchant_type: str = merchant_type
        self.response_url: str = response_url
        self.redirect_url: str = redirect_url
        self.base_data: Dict = {
            'store_id': self.store_id,
            'parts_count': self.parts_count,
            'merchant_type': self.merchant_type,
            'response_url': self.response_url,
            'redirect_url': self.redirect_url
        }

    @staticmethod
    def create_log(data: Dict, log_type: str) -> Log:
        data = prepare_log(data)
        data['type'] = log_type
        return Log.objects.create(**data)

    @staticmethod
    def str_to_sign(value: str):
        return b64encode(sha1(str.encode(value)).digest()).decode("utf-8")

    @staticmethod
    def get_redirect_url(token: str) -> str:
        return f'{API_REDIRECT_URL}?token={token}'

    @staticmethod
    def prepare_data(data: Dict) -> Dict:
        cleaned_data = {
            key: value for key, value in data.items() if value
        }
        return cleaned_data

    def create_signature(self, data: Dict) -> str:
        products = data['products']
        products_string = ''.join(
            [
                item['name'] +
                str(item['count']) +
                str(int(item['price'] * 100))
                for item in products
            ]
        )
        value = (
            self.password +
            self.store_id +
            str(data['order_id']) +
            str(int(data['amount'] * 100)) +
            str(self.parts_count) +
            self.merchant_type +
            self.response_url +
            self.redirect_url +
            products_string +
            self.password
        )
        return self.str_to_sign(value)

    def validate_signature(self, data: Dict) -> bool:
        signature1 = data['signature']
        signature2 = self.str_to_sign(
            self.password +
            data['storeId'] +
            data['orderId'] +
            data['state'] +
            data['message'] +
            self.password
        )
        return signature1 == signature2

    def payment_create(self, data: Dict) -> Dict:
        data.update(self.base_data)
        data['signature'] = self.create_signature(data)
        data = json.dumps(
            prepare_order(self.prepare_data(data)),
            ensure_ascii=False
        ).encode('utf-8')
        response = self.api_client.post(
            'payment/create',
            data
        )
        return response['result']
