from django.db import models
from django.utils.translation import ugettext_lazy as _

from payparts.consts import (
    SUCCESS, FAIL,
    CANCELED,
    STATE_CHOICES,
    LOG_CHOICES
)

__all__ = (
    'Log',
)


class Log(models.Model):
    type = models.CharField(
        _('Log type'),
        max_length=20,
        choices=LOG_CHOICES,
        blank=True
    )
    state = models.CharField(
        _('State'),
        max_length=20,
        choices=STATE_CHOICES,
        blank=True
    )
    store_id = models.CharField(
        _('Store id'),
        max_length=20,
        blank=True
    )
    order_id = models.CharField(
        _('Order id'),
        max_length=64,
        blank=True
    )
    token = models.CharField(
        _('Token'),
        max_length=32,
        blank=True
    )
    signature = models.CharField(
        _('Signature'),
        max_length=120,
        blank=True
    )
    message = models.TextField(
        _('Message'),
        blank=True
    )

    def __str__(self) -> str:
        if self.order_id and self.state:
            return f'{self.order_id}: {self.get_state_display()}'
        return str(self.pk)

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

    @property
    def is_success(self):
        return self.state == SUCCESS

    @property
    def is_fail(self):
        return self.state == FAIL

    @property
    def is_canceled(self):
        return self.state == CANCELED
