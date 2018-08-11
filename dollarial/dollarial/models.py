import logging

from bitfield import BitField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models, transaction

from dollarial import settings
from dollarial.constants import TransactionConstants
from dollarial.currency import Currency
from dollarial.fields import PriceField, CurrencyField


class User(AbstractUser):
    account_number = models.CharField(max_length=64, verbose_name="Account Number", unique=True)
    phone_number = models.CharField(max_length=32, blank=True, verbose_name="Phone Number")

    NOTIFICATION_TYPES = (
        ('S', 'sms'),
        ('E', 'email')
    )
    notification_preference = models.CharField(max_length=1, choices=NOTIFICATION_TYPES, default='S',
                                               verbose_name="Notification Preference")

    def get_wallet(self, currency):
        if currency not in Currency.get_all_currency_chars():
            logging.error("No such kind of currency %s" % currency)
            return None
        return Wallet.objects.get_or_create(user=self, currency=currency)[0]

    def get_credit(self, currency):
        return self.get_wallet(currency).credit

    def create_wallets(self):
        for currency in Currency.get_all_currency_chars():
            _, created = Wallet.objects.get_or_create(user=self, currency=currency)
            if not created:
                logging.warning("Wallet with currency %s already existed for user %s" % (currency, self))

    def create_relative_clerk(self, salary=0):
        return Clerk.objects.create(user=self, salary=salary)

    def __str__(self):
        return self.username


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, verbose_name="User")
    credit = PriceField(default=0, verbose_name="Credit")
    currency = CurrencyField(default='R', verbose_name="Currency")

    def __str__(self):
        return "%s(%s)" % (self.user.username, self.currency)

    class Meta:
        unique_together = ('user', 'currency')


class Clerk(models.Model):
    salary = models.PositiveIntegerField(default=0, verbose_name="Salary")
    is_employee = models.BooleanField(default=True, verbose_name="is Employee")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        return self.user.username


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_credit(self, currency):
        return self.user.get_credit(currency)

    def __str__(self):
        return self.user.username


@transaction.atomic
def _get_dollarial_company():
    try:
        dollarial = Company.objects.get(user__username="dollarial")
    except Company.DoesNotExist:
        dollarial_user = User.objects.create(
            username="dollarial",
            account_number="1234567890",
            email="dollarial@sharif.ir"
        )
        dollarial_user.create_wallets()
        dollarial = Company.objects.create(
            user=dollarial_user
        )
    return dollarial


def get_dollarial_company():
    return _get_dollarial_company()


def get_dollarial_user():
    return _get_dollarial_company().user


class PaymentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    min_amount = PriceField(blank=True, default=min(TransactionConstants.MIN_AMOUNT.values()),
                            verbose_name="Minimum Amount")
    max_amount = PriceField(blank=True, default=max(TransactionConstants.MAX_AMOUNT.values()),
                            verbose_name="Minimum Amount")
    price = PriceField(blank=True, default=0, verbose_name="Fixed Price")
    wage_percentage = models.PositiveSmallIntegerField(default=TransactionConstants.NORMAL_WAGE_PERCENTAGE,
                                                       validators=[MaxValueValidator(100)],
                                                       verbose_name="Wage Percentage")
    currency = CurrencyField(default='R', verbose_name="Currency")
    fixed_price = models.BooleanField(default=True, verbose_name="Fixed Price")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    required_fields = BitField(flags=(
        'general_info',
        'personal_info',
        'exam_info',
        'university_info'
    ))
    transaction_group = models.ForeignKey(PaymentGroup, blank=True, null=True, on_delete=models.CASCADE,
                                          verbose_name="Group")

    def __str__(self):
        return self.name
