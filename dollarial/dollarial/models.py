import logging

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from dollarial import settings
from dollarial.currency import Currency
from dollarial.fields import PriceField, CurrencyField
from kavenegar import *

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

    def get_wallet(self, currency):
        return self.user.get_wallet(currency)

    def create_wallets(self):
        self.user.create_wallets()

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


def send_sms_to_all_users(message):
    try:
        api = KavenegarAPI('457A5A6564762B35696C334E6D3957765672713035673D3D')
        params = {
            'sender': '',  # optinal
            'receptor': '',  # multiple mobile number, split by comma
            'message': message,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
