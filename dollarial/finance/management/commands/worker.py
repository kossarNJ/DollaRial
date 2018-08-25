from django.core.management.base import BaseCommand


def update_salary():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")


class Command(BaseCommand):
    def handle(self, **options):
        update_salary()