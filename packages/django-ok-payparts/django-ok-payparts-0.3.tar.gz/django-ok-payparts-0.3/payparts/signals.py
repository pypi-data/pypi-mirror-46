from django.dispatch import Signal

__all__ = (
    'pay_parts_success_callback',
    'pay_parts_invalid_callback'
)


pay_parts_success_callback = Signal(providing_args=["log", "request"])
pay_parts_invalid_callback = Signal(providing_args=["log", "request"])
