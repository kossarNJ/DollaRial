from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand
from django import db

from dollarial import notification
from finance.models import Transaction


@db.transaction.atomic
def fail_transactions():
    failed_time = timezone.now() - timedelta(hours=24)
    failed_transactions = Transaction.objects.filter(deleted=False, status='I', time__lte=failed_time)
    for transaction in failed_transactions:
        transaction.status = 'R'
        notification.send_notification_to_user(
            transaction.owner,
            subject='#%d Transaction Auto Reject' % transaction.id,
            message="Unfortunately, Your transaction did not receive any reviews after 24 hours." +
                    " Please submit your request again."
        )
        print("Transaction ", transaction, " failed automatically.")
        transaction.save()


class Command(BaseCommand):
    def handle(self, **options):
        fail_transactions()
