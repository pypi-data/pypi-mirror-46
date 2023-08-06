=================================
django-ok-payparts |PyPI version|
=================================

|Build Status| |Code Health| |Python Versions| |Requirements Status| |license| |PyPI downloads|

Simple django integration for API "Оплата Частями в Интернете": `Схема взаимодействия №1 (Создание платежа по сервису Оплата частями/Мгновенная рассрочка)`_.

Installation
============

Install with pip:

.. code:: shell

    $ pip install django-ok-payparts


Update INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...
        'payparts',
        ...
    ]


Add ``payparts.urls`` to your project urlpatterns:

.. code:: python

    urlpatterns = [
        ...
        path('', include('payparts.urls')),
        ...
    ]


Make migrations:

.. code:: shell

    $ python manage.py migrate


Available settings
==================

``PAYPARTS_API_PASSWORD`` - Password of your store.

``PAYPARTS_API_STORE_ID`` - Your store's ID.

``PAYPARTS_API_URL`` - Url for creation of a payment. By default: `https://payparts2.privatbank.ua/ipp/v2/`.

``PAYPARTS_API_REDIRECT_URL`` - Url to redirect after a success payment. By default: `https://payparts2.privatbank.ua/ipp/v2/payment`.

Usage
=====

How to create a payment
-----------------------

1. Prepare your order's data:

.. code:: python

    data = {
        "order_id": f"order-123",
        "amount": 400.00,
        "parts_count": 2,  # optional, default value is '2'
        "merchant_type": "II",  # optional, default value is 'II'
        "products": [
            {
                "name": "Телевизор",
                "count": 2,
                "price": 100.00
            },
            {
                "name": "Микроволновка",
                "count": 1,
                "price": 200.00
            }
        ],
        # also optional fields (can be set in your cabinet):
        "response_url": "http://shop.com/response",  
        "redirect_url": "http://shop.com/redirect",
    }


2. Get your redirect url:

.. code:: python

    from payparts.use_cases import GetRedirectUrlUseCase
    redirect_url = GetRedirectUrlUseCase().execute(data)


3. Redirect a user to the url.


How to process a callback
-------------------------

Whenever a callback is processed a signal will be sent with the result of the transaction.

There are two signals (``payparts.signals``):

1) ``pay_parts_success_callback`` - if signature is valid.
2) ``pay_parts_invalid_callback`` - if signature is not valid.

Connect the signals to actions to perform the needed operations when a successful payment is received:

.. code:: python

    from payparts.signals import pay_parts_success_callback, pay_parts_invalid_callback

    from orders.models import Order


    def success_callback(sender, log, request, **kwargs):
        # ensure success state
        if log.is_success:
            order = Order.objects.get(pk=log.order_id)
            order.set_success_payment_state()

    pay_parts_success_callback.connect(success_callback)


.. |PyPI version| image:: https://badge.fury.io/py/django-ok-payparts.svg
   :target: https://badge.fury.io/py/django-ok-payparts
.. |Build Status| image:: https://travis-ci.org/LowerDeez/ok-payparts.svg?branch=master
   :target: https://travis-ci.org/LowerDeez/ok-payparts
   :alt: Build status
.. |Code Health| image:: https://api.codacy.com/project/badge/Grade/ec55733ec684421aaee9e3a334c5f4a7    
   :target: https://www.codacy.com/app/LowerDeez/ok-payparts
   :alt: Code health
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/django-ok-payparts.svg
   :target: https://pypi.org/project/django-ok-payparts/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-ok-payparts.svg
   :alt: Software license
   :target: https://github.com/LowerDeez/ok-payparts/blob/master/LICENSE
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/django-ok-payparts.svg
   :alt: PyPI downloads
.. |Requirements Status| image:: https://requires.io/github/LowerDeez/ok-payparts/requirements.svg?branch=master


.. _Схема взаимодействия №1 (Создание платежа по сервису Оплата частями/Мгновенная рассрочка): https://bw.gitbooks.io/api-oc/content/pay.html