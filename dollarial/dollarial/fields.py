from django.db import models
from django import forms

from dollarial.currency import Currency


class PriceField(models.FloatField):
    def __init__(self, max_digits=None, decimal_places=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CurrencyField(models.CharField):
    def __init__(self, max_length=None, choices=None, *args, **kwargs):
        super().__init__(max_length=1, choices=Currency.choices(), *args, **kwargs)


class PriceFormField(forms.FloatField):
    pass


class CurrencyFormField(forms.CharField):
    def __init__(self, max_length=None, choices=None, *args, **kwargs):
        super().__init__(max_length=1, choices=Currency.choices(), *args, **kwargs)
