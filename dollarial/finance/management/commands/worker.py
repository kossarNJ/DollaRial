from django.core.management.base import BaseCommand
from django.db import transaction

from dollarial.models import Clerk, get_dollarial_company, get_dollarial_user
from dollarial.notification import send_email_to_user
from dollarial.settings import ADMIN_EMAIL
from finance.models import Transaction


@transaction.atomic
def update_salary():
    total = 0
    valid_clerk = Clerk.objects.filter(is_employee=True)

    for clerk in valid_clerk:
        total = total + clerk.salary
    company = get_dollarial_company()
    company_credit = company.get_credit("R")
    sum_all = 0
    salary_objects = []
    for clerk in valid_clerk:
        salary_object = Transaction(owner=clerk.user, amount=clerk.salary, currency='R', wage=0, status='A')
        payment_object = Transaction(owner=get_dollarial_user(), amount=-clerk.salary, currency='R', wage=0, status='A')
        salary_objects.append([salary_object, payment_object])
        sum_all += clerk.salary
    if sum_all > company_credit:
        send_email_to_user("Low Credit", "auto@dollarial.com", ADMIN_EMAIL,
                           "Your Credit is not enough to pay the salaries. Your Credit is " +
                           str(company_credit) + " and total salaries is " + str(total))
        raise Exception("Not enough credit to create salaries")

    else:
        for x, y in salary_objects:
            x.save()
            y.save()
        send_email_to_user("Salary paid", "auto@dollarial.com", ADMIN_EMAIL,
                           " Clerks Salary Paid. Current credit: " + str(company_credit - sum_all))


class Command(BaseCommand):
    def handle(self, **options):
        update_salary()
