from django.conf import settings

__all__ = (
    'API_PASSWORD',
    'API_STORE_ID',
    'API_BASE_URL',
    'API_REDIRECT_URL'
)


API_PASSWORD: str = getattr(
    settings,
    'PAYPARTS_API_PASSWORD',
    None
)

API_STORE_ID: str = getattr(
    settings,
    'PAYPARTS_API_STORE_ID',
    None
)

API_BASE_URL: str = getattr(
    settings,
    'PAYPARTS_API_URL',
    'https://payparts2.privatbank.ua/ipp/v2/'
)

API_REDIRECT_URL: str = getattr(
    settings,
    'PAYPARTS_API_REDIRECT_URL',
    'https://payparts2.privatbank.ua/ipp/v2/payment'
)
