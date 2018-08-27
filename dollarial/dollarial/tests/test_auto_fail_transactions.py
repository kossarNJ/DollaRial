from django.test import TestCase
from freezegun import freeze_time

from dollarial.models import get_dollarial_user
from finance.management.commands import autofail
from finance.models import Transaction


class AutoFailTestCase(TestCase):
    @staticmethod
    def __create_transactions(count):
        for i in range(count):
            Transaction.objects.create(
                owner=get_dollarial_user(),
                amount=10,
                currency='R',
                status='I'
            )

    @staticmethod
    def __run_scheduled_task():
        autofail.fail_transactions()

    @staticmethod
    def __count_failed_transactions():
        return Transaction.objects.filter(status='R').count()

    def test_auto_fail(self):
        # setup
        with freeze_time("2012-01-01 00:00"):
            self.__create_transactions(5)
        with freeze_time("2012-01-10 00:00"):
            self.__create_transactions(5)
        with freeze_time("2012-01-10 01:00"):
            self.__create_transactions(5)
        # check
        with freeze_time("2012-01-10 23:00"):
            self.__run_scheduled_task()
            cnt = self.__count_failed_transactions()
            self.assertEqual(cnt, 5)
        with freeze_time("2012-01-11 00:00"):
            self.__run_scheduled_task()
            cnt = self.__count_failed_transactions()
            self.assertEqual(cnt, 10)
        with freeze_time("2012-01-11 00:59"):
            self.__run_scheduled_task()
            cnt = self.__count_failed_transactions()
            self.assertEqual(cnt, 10)
        with freeze_time("2012-01-11 01:00"):
            self.__run_scheduled_task()
            cnt = self.__count_failed_transactions()
            self.assertEqual(cnt, 15)

    def test_auto_fail_very_late(self):
        with freeze_time("2012-01-01 00:00"):
            self.__create_transactions(5)
        with freeze_time("2013-01-10 23:00"):
            self.__run_scheduled_task()
            cnt = self.__count_failed_transactions()
            self.assertEqual(cnt, 5)
