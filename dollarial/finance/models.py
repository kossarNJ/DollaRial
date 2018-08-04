from datetime import datetime
from enum import Enum

from django.db import models
from django.db.models import CASCADE, Sum
from polymorphic.models import PolymorphicModel

from dollarial import settings
from dollarial.fields import PriceField, CurrencyField


class Transaction(PolymorphicModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name="Owner")
    amount = PriceField(verbose_name="Amount")
    currency = CurrencyField(verbose_name="Currency")
    date = models.DateTimeField(default=datetime.now, verbose_name="Date")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    def __str__(self):
        return "%s %s%s" % (self.owner.username, self.amount, self.currency)

    def save(self, *args, **kwargs,):
        super().save(*args, **kwargs)
        update_credit(self.owner, self.currency)


class BankPayment(Transaction):
    class PaymentType(Enum):
        DEPOSIT = 1
        CHARGE = 2

    @property
    def payment_type(self):
        if self.amount < 0:
            return self.PaymentType.DEPOSIT
        else:
            return self.PaymentType.CHARGE

    def __str__(self):
        return "%s %s%s (%s)" % (self.owner.username, self.amount, self.currency, self.payment_type)


class Exchange(Transaction):
    final_amount = PriceField(verbose_name="Final Amount")
    final_currency = CurrencyField(verbose_name="Final Currency")

    def __str__(self):
        return "%s %s%s->%s%s" % (self.amount, self.currency, self.final_amount, self.final_currency)


def update_credit(user, currency):
    wallet = user.get_wallet(currency)
    wallet.credit = \
        Transaction.objects.filter(owner=user, deleted=False).aggregate(Sum('amount'))['amount__sum'] or 0
    wallet.save()
