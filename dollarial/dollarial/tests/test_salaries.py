from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time

from dollarial.scheduled_tasks import run_scheduled_tasks


class AutoFailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: create reviewers
        # reviewer1 active 1000
        # reviewer2 active 1200
        # reviewer3 active 1300
        # reviewer4 inactive 2000
        pass

    def __assert_transaction_count(self, prediction):
        cnt = 0  # Transaction count
        self.assertEqual(cnt, prediction)

    @staticmethod
    def __find_transaction_by_username(username):
        # TODO: return Transactions.objects.filter(username=username)
        return []

    def test_auto_creation(self):
        with freeze_time("2012-01-01 00:00"):
            run_scheduled_tasks(datetime.now())
        self.__assert_transaction_count(3)
        self.assertIsNotNone(self.__find_transaction_by_username('reviewer1'))
        self.assertIsNotNone(self.__find_transaction_by_username('reviewer2'))
        self.assertIsNotNone(self.__find_transaction_by_username('reviewer3'))
        self.assertIsNone(self.__find_transaction_by_username('reviewer4'))

    def test_salary_amount(self):
        with freeze_time("2012-01-01 00:00"):
            run_scheduled_tasks(datetime.now())
        for username, salary in [('reviewer1', 1000), ('reviewer2', 1200), ('reviewer3', 1300)]:
            transaction = self.__find_transaction_by_username(username).last
            self.assertEqual(transaction.salary, salary)

