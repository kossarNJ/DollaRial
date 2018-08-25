from django.db import transaction

from dollarial.models import User
from finance import models as finance_models


@transaction.atomic
def create_internal_payment(user, amount, destination):
    if amount <= 0:
        raise ValueError("Amount should be positive")

    internal_payment = finance_models.InternalPayment(
        owner=user,
        amount=-amount,
        currency='R',
        wage=0,
        status='A',
    )
    destination_user = User.get_or_create_automatic_user(destination)
    reverse_object = finance_models.ReverseInternalPayment(
        owner=destination_user,
        amount=amount,
        currency='R',
        wage=0,
        status='A'
    )
    reverse_object.save()
    internal_payment.reverse_payment = reverse_object
    internal_payment.save()


@transaction.atomic
def check_enough_credit(amount, currency, user):
    credit = user.get_credit(currency)
    return credit >= 0 and credit >= amount


@transaction.atomic
def check_validity_of_new_transaction(transaction_object):
    return check_enough_credit(
        amount=transaction_object.amount * -1,
        currency=transaction_object.currency,
        user=transaction_object.owner
    )
