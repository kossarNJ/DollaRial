from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time

from dollarial import scheduled_tasks


class CreditAlertTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: Create account for Company in DB
        class Company:
            def __init__(self):
                self.credit = 10

        cls.company = Company()

    def test_low_credit_alert(self):
        self.company.credit = 100
        with freeze_time("2012-01-01 00:00"):
            scheduled_tasks.run_scheduled_tasks(datetime.now())
        self.assertEqual(Alerts.objects.count(), 1)

    def test_high_credit_alert(self):
        self.company.credit = 10000000
        with freeze_time("2012-01-01 00:00"):
            scheduled_tasks.run_scheduled_tasks(datetime.now())
        self.assertEqual(Alerts.objects.count(), 0)

    def test_near_credit_alert(self):
        self.company.credit = 1000000
        with freeze_time("2012-01-01 00:00"):
            scheduled_tasks.run_scheduled_tasks(datetime.now())
        self.assertEqual(Alerts.objects.count(), 0)
        self.company.credit = self.company.credit - 1
        with freeze_time("2012-01-02 00:00"):
            scheduled_tasks.run_scheduled_tasks(datetime.now())
        self.assertEqual(Alerts.objects.count(), 1)
