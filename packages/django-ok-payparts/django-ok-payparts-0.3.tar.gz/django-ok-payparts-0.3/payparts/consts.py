from django.utils.translation import ugettext_lazy as _

__all__ = (
    'MERCHANT_TYPES',
    'DEFAULT_MERCHANT_TYPE',
    'DEFAULT_PARTS_COUNT',
    'CREATED',
    'SUCCESS',
    'CANCELED',
    'FAIL',
    'CLIENT_WAIT',
    'OTP_WAITING',
    'PP_CREATION',
    'LOCKED',
    'STATE_CHOICES',
    'LOG_CHOICES'
)


MERCHANT_TYPES = (
    ('II', 'II'),
    ('PP', 'PP'),
    ('PB', 'PB'),
    ('IA', 'IA')
)

DEFAULT_MERCHANT_TYPE = 'II'
DEFAULT_PARTS_COUNT = 2

CREATED = 'CREATED'
SUCCESS = 'SUCCESS'
CANCELED = 'CANCELED'
FAIL = 'FAIL'
CLIENT_WAIT = 'CLIENT_WAIT'
OTP_WAITING = 'OTP_WAITING'
PP_CREATION = 'PP_CREATION'
LOCKED = 'LOCKED'


STATE_CHOICES = (
    (CREATED, _('Created')),
    (SUCCESS, _('Success')),
    (FAIL, _('Fail')),
    (CANCELED, _('Canceled')),
    (CLIENT_WAIT, _('Client wait')),
    (OTP_WAITING, _('OTP waiting')),
    (PP_CREATION, _('PP creation')),
    (LOCKED, _('Locked'))
)

LOG_CHOICES = (
    ('payment_create', _('Creation of payment')),
    ('callback', _('Payment callback'))
)
