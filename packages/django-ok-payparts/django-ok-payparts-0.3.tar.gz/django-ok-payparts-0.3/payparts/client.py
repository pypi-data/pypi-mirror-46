from typing import Dict

import requests

from payparts.settings import API_BASE_URL

__all__ = (
    'PayPartsAPIClient',
)


class PayPartsAPIClient:
    @staticmethod
    def get_base_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "UTF-8"
        }

    @staticmethod
    def construct_url(*args) -> str:
        """
        Returns url with joined args as parts of url.

        Args:
            *args: part of url.

        Returns:
            str: URL
        """
        url = API_BASE_URL

        if not args:
            return url

        joined_args = '/'.join([x.strip('/') for x in args]) + '/'

        return f'{url}{joined_args}'

    def post(
        self,
        path: str,
        data: Dict = None,
        headers: Dict = None
    ):
        """
        Private method used to send request to the remote REST API server.

        Args:
            path (str): Corresponding relative path to send request.
            data (Dict, optional): Params to send.
            headers (Dict, optional): Request headers.

        Returns:
            Response: requests' response instance.

        Raises:
            AttributeError: Unsupported method was used.
        """
        url = self.construct_url(path)

        if headers is None:
            headers = {}

        headers.update(self.get_base_headers())

        response = requests.post(
            url=url,
            data=data,
            headers=headers
        )

        return {
            "result": response.json(),
            "status_code": response.status_code
        }
