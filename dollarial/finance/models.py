from datetime import datetime
from enum import Enum

from django.db import models
from polymorphic.models import PolymorphicModel

from dollarial import settings
from dollarial.fields import PriceField, CurrencyField
from dollarial.models import PaymentType


class Transaction(PolymorphicModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner")
    amount = PriceField(verbose_name="Amount")
    currency = CurrencyField(verbose_name="Currency")
    date = models.DateTimeField(default=datetime.now, verbose_name="Date")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")
    wage = PriceField(default=0, verbose_name="Wage")

    TRANSACTION_STATUS = (
        ('I', 'In Review'),
        ('R', 'Rejected'),
        ('A', 'Accepted')
    )
    status = models.CharField(max_length=1, choices=TRANSACTION_STATUS, default='I', verbose_name="Status")

    def __str__(self):
        return "%s %s%s (%s)" % (self.owner.username, self.amount, self.currency, self.status)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_credit(self.owner, self.currency)


class BankPayment(Transaction):
    class BankPaymentType(Enum):
        DEPOSIT = 1
        CHARGE = 2

    @property
    def payment_type(self):
        if self.amount < 0:
            return self.BankPaymentType.DEPOSIT
        else:
            return self.BankPaymentType.CHARGE

    def __str__(self):
        return "%s (%s)" % (super().__str__(), self.payment_type)


class Exchange(Transaction):
    final_amount = PriceField(verbose_name="Final Amount")
    final_currency = CurrencyField(verbose_name="Final Currency")

    def __str__(self):
        return "%s %s%s->%s%s" % (self.amount, self.currency, self.final_amount, self.final_currency)


class FormPayment(Transaction):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, verbose_name="Payment Type")

    # general info
    first_name = models.CharField(max_length=63, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=63, blank=True, verbose_name="Last Name")
    phone_number = models.CharField(max_length=32, blank=True, verbose_name="Phone Number")

    # personal info
    security_number = models.CharField(max_length=10, blank=True, verbose_name="Security Number")
    passport_number = models.CharField(max_length=10, blank=True, verbose_name="Passport Number")

    # exam info
    exam_username = models.CharField(max_length=63, blank=True, verbose_name="Exam Username")
    exam_password = models.CharField(max_length=63, blank=True, verbose_name="Exam Password")
    exam_date = models.DateField(null=True, blank=True, verbose_name="Exam Date")
    exam_country = models.CharField(max_length=63, blank=True, verbose_name="Exam Country")
    exam_city = models.CharField(max_length=63, blank=True, verbose_name="Exam City")
    exam_center = models.CharField(max_length=256, blank=True, verbose_name="Exam Center")

    # university info
    university_link = models.URLField(blank=True, verbose_name="University Link")
    university_username = models.CharField(max_length=63, blank=True, verbose_name="University Username")
    university_password = models.CharField(max_length=63, blank=True, verbose_name="University Password")

    @property
    def final_amount(self):
        return self.amount - self.wage

    flag_related_fields = {
        'general_info': ('first_name', 'last_name', 'phone_number'),
        'personal_info': ('security_number', 'passport_number'),
        'exam_info': ('exam_username', 'exam_password', 'exam_date', 'exam_country', 'exam_city',
                      'exam_center'),
        'university_info': ('university_link', 'university_username', 'university_password')
    }


def update_credit(user, currency):
    wallet = user.get_wallet(currency)
    wallet.credit = \
        Transaction.objects.filter(
            owner=user,
            deleted=False,
            status='A',
            currency=wallet.currency
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
    wallet.save()
