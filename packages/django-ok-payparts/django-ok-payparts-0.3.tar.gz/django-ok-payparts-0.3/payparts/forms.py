from django import forms

from payparts.consts import MERCHANT_TYPES

__all__ = (
    'PayloadForm',
    'ProductForm'
)


class PayloadForm(forms.Form):
    order_id = forms.CharField(max_length=64)
    amount = forms.FloatField(min_value=300, max_value=50000)
    parts_count = forms.IntegerField(min_value=2, max_value=25, required=False)
    merchant_type = forms.ChoiceField(choices=MERCHANT_TYPES, required=False)
    response_url = forms.CharField(required=False, max_length=255)
    redirect_url = forms.CharField(required=False, max_length=255)


class ProductForm(forms.Form):
    name = forms.CharField(max_length=128)
    count = forms.IntegerField(min_value=1)
    price = forms.FloatField(min_value=0.01)
