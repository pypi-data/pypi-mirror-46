from functools import partial

from trafaret import Dict, String, List, Key, Int, Float

__all__ = (
    'ORDER',
    'LOG',
    'prepare_log',
    'prepare_order'
)

ORDER = Dict({
    Key('store_id') >> 'storeId': String,
    Key('order_id') >> 'orderId': String,
    Key('amount') >> 'amount': Float,
    Key('parts_count') >> 'partsCount': Int,
    Key('merchant_type') >> 'merchantType': String,
    Key('products') >> 'products': List(
        Dict({
            Key('name') >> 'name': String,
            Key('count') >> 'count': Int,
            Key('price') >> 'price': Float,
        }, ignore_extra='*'),
        min_length=1
    ),
    Key('response_url', optional=True) >> 'responseUrl': String,
    Key('redirect_url', optional=True) >> 'redirectUrl': String,
    Key('signature') >> 'signature': String
}, ignore_extra='*')


LOG = Dict({
    Key('state') >> 'state': String,
    Key('storeId') >> 'store_id': String,
    Key('orderId') >> 'order_id': String,
    Key('token', optional=True) >> 'token': String,
    Key('message', optional=True) >> 'message': String,
    Key('signature') >> 'signature': String
}, ignore_extra='*')


def _extract(template, *args, **kwargs):
    return template.transform(*args, **kwargs)


prepare_order = partial(_extract, ORDER)
prepare_log = partial(_extract, LOG)
