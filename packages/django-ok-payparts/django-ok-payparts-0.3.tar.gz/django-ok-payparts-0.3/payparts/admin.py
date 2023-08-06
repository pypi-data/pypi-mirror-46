from django.contrib import admin

from payparts.models import Log

__all__ = (
    'LogAdmin',
)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'type',
        'state'
    ]
    list_filter = [
        'type',
        'state'
    ]
