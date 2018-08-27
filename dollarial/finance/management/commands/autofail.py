from django.core.management.base import BaseCommand


def fail_transactions():
    print("transactions failed")


class Command(BaseCommand):
    def handle(self, **options):
        fail_transactions()