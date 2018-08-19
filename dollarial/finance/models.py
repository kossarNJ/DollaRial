from enum import Enum

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from dollarial import settings
from dollarial.currency import Currency
from dollarial.fields import PriceField, CurrencyField
from dollarial.models import PaymentType


class Transaction(PolymorphicModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner")
    amount = PriceField(verbose_name="Amount")
    currency = CurrencyField(verbose_name="Currency")
    time = models.DateTimeField(default=timezone.now, verbose_name="Time")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")
    wage = PriceField(default=0, verbose_name="Wage")

    @property
    def sent_amount(self):
        return -self.amount - self.wage

    def get_display_data(self):
        return [
            ('Owner', self.owner.username),
            ('Time', self.time),
            ('Amount', "%s%s" % (self.amount, self.get_currency_display())),
            ('Wage', "%s%s" % (self.wage, self.get_currency_display())),
            ('Deleted', self.deleted),
            ('Status', self.get_status_display())
        ]

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

    def get_display_data(self):
        data = super().get_display_data()
        data.extend([
            ('Type', 'Charge' if self.payment_type is self.BankPaymentType.CHARGE else 'Deposit'),
        ])
        return data

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


class ExternalPayment(Transaction):
    destination_number = models.CharField(max_length=63, verbose_name="Destination Account Number")

    def get_display_data(self):
        data = super().get_display_data()
        data.extend([
            ('Destination', self.destination_number),
            ('Sent Amount', self.sent_amount)
        ])
        return data

    def __str__(self):
        return "%s to %s" % (super().__str__(), self.destination_number)


class ReverseInternalPayment(Transaction):
    def get_display_data(self):
        data = super().get_display_data()
        data.extend([
            ('Sender', self.internalpayment.owner.account_number),
        ])
        return data


class InternalPayment(Transaction):
    reverse_payment = models.OneToOneField(ReverseInternalPayment, on_delete=models.CASCADE,
                                           null=False, verbose_name="Reverse Payment")

    def get_display_data(self):
        data = super().get_display_data()
        data.extend([
            ('Destination', self.reverse_payment.owner.account_number),
            ('Sent Amount', self.sent_amount)
        ])
        return data


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

    flag_related_fields = {
        'general_info': ('first_name', 'last_name', 'phone_number'),
        'personal_info': ('security_number', 'passport_number'),
        'exam_info': ('exam_username', 'exam_password', 'exam_date', 'exam_country', 'exam_city',
                      'exam_center'),
        'university_info': ('university_link', 'university_username', 'university_password')
    }

    def get_display_data(self):
        data = super().get_display_data()
        data.extend([
            ('Payment Type', "%s (%s)" % (self.payment_type.name, self.payment_type.id)),
        ])
        for flag, value in self.payment_type.required_fields:
            if value:
                for field in FormPayment.flag_related_fields[flag]:
                    data.append(
                        (self._meta.get_field(field).verbose_name, getattr(self, field))
                    )
        return data


def update_credit(user, currency):
    wallet = user.get_wallet(currency)
    wallet.credit = \
        Transaction.objects.filter(
            owner=user,
            deleted=False,
            status__in=['A', 'I'],
            currency=wallet.currency
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
    wallet.save()


def update_credit_all(user):
    for c in Currency.get_all_currency_chars():
        update_credit(user, c)
