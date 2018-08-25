import logging

from bitfield import BitField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models, transaction

from dollarial import settings
from dollarial.constants import TransactionConstants
from dollarial.currency import Currency
from dollarial.fields import PriceField, CurrencyField
from kavenegar import *
import sendgrid
from dollarial.settings import SEND_GRID
from sendgrid.helpers.mail import *


class User(AbstractUser):
    account_number = models.CharField(max_length=64, verbose_name="Account Number")
    phone_number = models.CharField(max_length=32, blank=True, verbose_name="Phone Number")
    automatic_user = models.BooleanField(default=False, verbose_name="Automatically Created")

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

    @transaction.atomic
    def update_relative_automatic_user_transactions(self):
        if self.automatic_user:
            return
        relative_automatic_user = User.objects.filter(account_number=self.account_number,
                                                      automatic_user=True)
        if not relative_automatic_user.count():
            return
        relative_automatic_user = relative_automatic_user.get()

        from finance.models import Transaction, update_credit_all

        transactions = Transaction.objects.filter(owner_id=relative_automatic_user.id)
        if transactions.count():
            transactions.update(owner=self)
            update_credit_all(self)

    @classmethod
    def get_or_create_automatic_user(cls, account_number):
        users = cls.objects.filter(account_number=account_number)
        if users.count() == 0:
            user = User.objects.create(
                account_number=account_number,
                automatic_user=True,
                username="Automatic %s" % account_number,
                is_active=False
            )
            return user
        elif users.count() > 1:
            return users.get(automatic_user=False)
        else:
            return users.get()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_relative_automatic_user_transactions()

    class Meta:
        unique_together = ('automatic_user', 'account_number',)


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


class PaymentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    min_amount = PriceField(null=True, default=min(TransactionConstants.MIN_AMOUNT.values()),
                            verbose_name="Minimum Amount")
    max_amount = PriceField(null=True, default=max(TransactionConstants.MAX_AMOUNT.values()),
                            verbose_name="Maximum Amount")
    price = PriceField(null=True, default=0, verbose_name="Fixed Price")
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

    @property
    def currency_sign(self):
        return Currency.get_by_char(self.currency).sign

    def __str__(self):
        return self.name


def send_sms_to_user(number, message):
    try:
        api = KavenegarAPI('457A5A6564762B35696C334E6D3957765672713035673D3D')
        params = {
            'sender': '',  # optinal
            'receptor': number,  # multiple mobile number, split by comma
            'message': message,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_email_to_user(subject, from_email, to_email, message):

    sg = sendgrid.SendGridAPIClient(
        apikey=SEND_GRID)
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())