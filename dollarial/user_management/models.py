from django.contrib.auth.models import AbstractUser
from django.db import models

from dollarial import settings

import logging


class User(AbstractUser):
    account_number = models.CharField(max_length=64, verbose_name="Account Number", unique=True)
    phone_number = models.CharField(max_length=32, blank=True, verbose_name="Phone Number")
    banned = models.BooleanField(default=False, verbose_name="Banned")

    NOTIFICATION_TYPES = (
        ('S', 'sms'),
        ('E', 'email')
    )
    notification_preference = models.CharField(max_length=1, choices=NOTIFICATION_TYPES, default='S',
                                               verbose_name="Notification Preference")

    def get_wallet(self, currency):
        if currency not in Wallet.CURRENCIES:
            logging.error("No such kind of currency %s" % currency)
            return None
        return Wallet.objects.get_or_create(user=self, currency=currency)[0]

    def create_wallets(self):
        for currency in Wallet.CURRENCIES:
            _, created = Wallet.objects.get_or_create(user=self, currency=currency)
            if not created:
                logging.warning("Wallet with currency %s already existed for user %s" % (currency, self))

    def __str__(self):
        return self.username


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, verbose_name="User")
    credit = models.BigIntegerField(default=0, verbose_name="credit")

    CURRENCY_CHOICES = (
        ('R', 'Rial'),
        ('D', 'Dollar'),
        ('E', 'Euro')
    )
    CURRENCIES = [x for x, y in CURRENCY_CHOICES]
    currency = models.CharField(max_length=1, choices=CURRENCY_CHOICES, default='R')

    def __str__(self):
        return "%s(%s)" % (self.user.username, self.currency)

    class Meta:
        unique_together = ('user', 'currency')


class Clerk(models.Model):
    salary = models.PositiveIntegerField(default=0, verbose_name="Salary")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
