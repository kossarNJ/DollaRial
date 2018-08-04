from django.db.models import DecimalField, CharField

from dollarial.currency import Currency


class PriceField(DecimalField):
    def __init__(self, max_digits=None, decimal_places=None, *args, **kwargs):
        super().__init__(max_digits=12, decimal_places=2, *args, **kwargs)


class CurrencyField(CharField):
    def __init__(self, max_length=None, choices=None, *args, **kwargs):
        super().__init__(max_length=1, choices=Currency.choices())
