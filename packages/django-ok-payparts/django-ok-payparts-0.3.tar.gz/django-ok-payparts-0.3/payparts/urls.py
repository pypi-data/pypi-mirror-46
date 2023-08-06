from django.urls import path

from payparts.views import PayPartsCallbackView

app_name = 'pay-parts'

urlpatterns = [
    path('pay-parts/callback/', PayPartsCallbackView.as_view(), name='callback')
]
