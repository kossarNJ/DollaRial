from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.currency import Currency
from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings

from finance.models import Transaction


class UserTransactionListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username="kossar",
                                             email="k_na@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.__create_transactions()
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/transactions/'))

    @staticmethod
    def __create_transactions():
        user = User.objects.get(username="kossar")
        transaction1 = Transaction(owner=user, amount="300", currency="D")
        transaction1.save()
        transaction2 = Transaction(owner=user, amount="30", currency="E")
        transaction2.save()
        transaction3 = Transaction(owner=user, amount="30000", currency="R")
        transaction3.save()

    def login(self):
        user = User.objects.get(username="kossar")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(username="kossar").id
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        }

        self.selenium.add_cookie(cookie)
        self.selenium.refresh()
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/transactions/'))

    def __get_transaction(self):
        class TransactionItem(object):
            def __init__(self, transaction_id, transaction_time, transaction_amount,
                         transaction_currency, transaction_status):
                self.transaction_id = transaction_id
                self.transaction_time = transaction_time
                self.transaction_amount = transaction_amount
                self.transaction_currency = transaction_currency
                self.transaction_status = transaction_status

        transactions = Transaction.objects.all()
        result = []
        for tr in transactions:
            result += [TransactionItem(tr.id, tr.time, tr.amount, tr.currency, tr.status)]
        return result

    def __get_page(self):
        class TransactionListPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = []
                self.amount = []
                self.currency = []
                self.status = []
                for i in range(1, 4):
                    self.id += [self.selenium.find_element_by_id('transaction_id_' + str(i))]
                    self.amount += [self.selenium.find_element_by_id('transaction_amount_' + str(i))]
                    self.currency += [
                        self.selenium.find_element_by_id('transaction_currency_' + str(i))]
                    self.status += [self.selenium.find_element_by_id('transaction_status_' + str(i))]

        return TransactionListPage(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        self.login()
        self.__create_transactions()
        transactions = self.__get_transaction()
        page = self.__get_page()
        for i in range(3):
            self.assertIn(str(transactions[i].transaction_id), self.__get_text(page.id[i]))
            self.assertIn(str(transactions[i].transaction_amount), self.__get_text(page.amount[i]))
            self.assertIn(Currency.get_by_char(transactions[i].transaction_currency[0]).sign,
                          self.__get_text(page.currency[i]))
            self.assertIn(transactions[i].transaction_status, self.__get_text(page.status[i]))
