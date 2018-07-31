from django.contrib.auth.models import AbstractUser
from django.db import models

from dollarial import settings


class User(AbstractUser):
    account_number = models.CharField(max_length=64, verbose_name="Account Number", unique=True)
    phone_number = models.CharField(max_length=32, blank=True, verbose_name="Phone Number")
    banned = models.BooleanField(default=False, verbose_name="Banned")

    NOTIFICATION_TYPES = (
        ('S', 'sms'),
        ('E', 'email')
    )
    notification_preference = models.CharField(max_length=1, choices=NOTIFICATION_TYPES, default='S')

    def __str__(self):
        return self.username


class Clerk(models.Model):
    salary = models.PositiveIntegerField(default=0, verbose_name="Salary")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
