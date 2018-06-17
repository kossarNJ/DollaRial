from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time

from dollarial.scheduled_tasks import run_scheduled_tasks


class AutoFailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: create users and transaction types
        pass

    @staticmethod
    def __create_transactions(count):
        for i in range(count):
            # TODO: create transactions
            pass

    def test_auto_fail(self):
        with freeze_time("2012-01-01 00:00"):
            self.__create_transactions(5)
        with freeze_time("2012-01-10 00:00"):
            self.__create_transactions(5)
        with freeze_time("2012-01-10 01:00"):
            self.__create_transactions(5)
        with freeze_time("2012-01-10 23:00"):
            run_scheduled_tasks(datetime.now())
            cnt = 0  # TODO: cnt = Transactions.objects.filter(status='F')
            self.assertEqual(cnt, 5)
        with freeze_time("2012-01-11 00:00"):
            run_scheduled_tasks(datetime.now())
            cnt = 0  # TODO: cnt = Transactions.objects.filter(status='F')
            self.assertEqual(cnt, 10)
        with freeze_time("2012-01-11 00:59"):
            run_scheduled_tasks(datetime.now())
            cnt = 0  # TODO: cnt = Transactions.objects.filter(status='F')
            self.assertEqual(cnt, 10)
        with freeze_time("2012-01-11 01:00"):
            run_scheduled_tasks(datetime.now())
            cnt = 0  # TODO: cnt = Transactions.objects.filter(status='F')
            self.assertEqual(cnt, 15)

    def test_auto_fail_very_late(self):
        with freeze_time("2012-01-01 00:00"):
            self.__create_transactions(5)
        with freeze_time("2013-01-10 23:00"):
            run_scheduled_tasks(datetime.now())
            cnt = 0  # TODO: cnt = Transactions.objects.filter(status='F')
            self.assertEqual(cnt, 5)
