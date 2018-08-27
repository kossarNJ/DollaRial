from django.test import TestCase
from freezegun import freeze_time

from dollarial.models import User, Clerk, get_dollarial_company
from finance.management.commands import worker
from finance.models import Transaction


class AutoFailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        reviewer1 = User.objects.create_superuser(
            username="reviewer1",
            email="k_na@gmail.com",
            password="likeicare",
            phone_number="09147898557",
            account_number="1234567812345678",
            notification_preference="S")
        reviewer2 = User.objects.create_user(
            username="reviewer2",
            email="k_naa@gmail.com",
            password="likeicare",
            phone_number="09147898557",
            account_number="1234432112344321",
            notification_preference="S")
        reviewer3 = User.objects.create_user(
            username="reviewer3",
            email="soroush@gmail.com",
            password="likeicare",
            phone_number="09147898557",
            account_number="1234567887654321",
            notification_preference="S")
        reviewer4 = User.objects.create_user(
            username="reviewer4",
            email="soroush2@gmail.com",
            password="likeicare",
            phone_number="09147898557",
            account_number="1212334567887654321",
            notification_preference="S")
        Clerk.objects.create(
            user=reviewer1,
            salary=1000
        )
        Clerk.objects.create(
            user=reviewer2,
            salary=1200
        )
        Clerk.objects.create(
            user=reviewer3,
            salary=1300
        )
        Clerk.objects.create(
            user=reviewer4,
            is_employee=False,
            salary=2000
        )
        Transaction.objects.create(
            owner=get_dollarial_company().user,
            amount=2000000,
            currency='R',
        )

    def __assert_transaction_count(self, prediction):
        cnt = Transaction.objects.count()
        print(Transaction.objects.all())
        self.assertEqual(cnt, prediction)

    @staticmethod
    def __find_transaction_by_username(username):
        return Transaction.objects.filter(owner__username=username)

    def test_auto_creation(self):
        with freeze_time("2012-01-01 00:00"):
            worker.update_salary()
        self.assertEqual(self.__find_transaction_by_username('reviewer1').count(), 1)
        self.assertEqual(self.__find_transaction_by_username('reviewer2').count(), 1)
        self.assertEqual(self.__find_transaction_by_username('reviewer3').count(), 1)
        self.assertEqual(self.__find_transaction_by_username('reviewer4').count(), 0)
        self.assertEqual(self.__find_transaction_by_username('dollarial').count(), 4)
        self.__assert_transaction_count(7)

    def test_salary_amount(self):
        with freeze_time("2012-01-01 00:00"):
            worker.update_salary()
        for username, salary in [('reviewer1', 1000), ('reviewer2', 1200), ('reviewer3', 1300)]:
            transaction = self.__find_transaction_by_username(username)[0]
            self.assertEqual(transaction.amount, salary)
