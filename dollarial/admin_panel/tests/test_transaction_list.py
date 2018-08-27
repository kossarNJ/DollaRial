from importlib import import_module
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.firefox.webdriver import WebDriver
from dollarial.currency import Currency
from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings

from finance.models import Transaction


class TransactionListTest(StaticLiveServerTestCase):
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
        self.user = User.objects.create_superuser(username="kossar_admin",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234567812345678",
                                                  notification_preference="S")
        self.user = User.objects.create_user(username="kossar",
                                             email="k_naa@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.user = User.objects.create_user(username="soroush",
                                             email="soroush@gmail.com",
                                             password="likeicare",
                                             first_name="soroush",
                                             last_name="ebadian",
                                             phone_number="09147898557",
                                             account_number="1234567887654321",
                                             notification_preference="S")
        self.__create_transactions()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/'))

    @staticmethod
    def __create_transactions():
        user_k = User.objects.get(username="kossar")
        user_s = User.objects.get(username="soroush")
        transaction1 = Transaction(owner=user_k, amount="300", currency="D")
        transaction1.save()
        transaction2 = Transaction(owner=user_k, amount="30", currency="E")
        transaction2.save()
        transaction3 = Transaction(owner=user_k, amount="30000", currency="R")
        transaction3.save()
        transaction4 = Transaction(owner=user_s, amount="40000", currency="R")
        transaction4.save()

    def login(self):
        user = User.objects.get(username="kossar_admin")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(username="kossar_admin").id
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/'))

    def __get_transaction(self):
        class TransactionItem(object):
            def __init__(self, transaction_id, transaction_amount,
                         transaction_currency, transaction_wage, transaction_owner,
                         transaction_status, transaction_deleted):
                self.transaction_id = transaction_id
                self.transaction_amount = transaction_amount
                self.transaction_currency = transaction_currency
                self.transaction_wage = transaction_wage
                self.transaction_owner = transaction_owner
                self.transaction_status = transaction_status
                self.transaction_deleted = transaction_deleted

        transactions = Transaction.objects.all()
        result = []
        for tr in transactions:
            result += [TransactionItem(tr.id, tr.amount, tr.currency, tr.wage, tr.owner, tr.status, tr.deleted)]
        return result

    def __get_page(self):
        class TransactionListPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = []
                self.amount = []
                self.currency = []
                self.wage = []
                self.owner = []
                self.status = []
                self.deleted = []
                for i in range(1, 4):
                    self.id += [self.selenium.find_element_by_id('transaction_id_' + str(i))]
                    self.amount += [self.selenium.find_element_by_id('transaction_amount_' + str(i))]
                    self.currency += [
                        self.selenium.find_element_by_id('transaction_currency_' + str(i))]
                    self.wage += [self.selenium.find_element_by_id('transaction_wage_' + str(i))]
                    self.owner += [self.selenium.find_element_by_id('transaction_owner_' + str(i))]
                    self.status += [self.selenium.find_element_by_id('transaction_status_' + str(i))]
                    self.deleted += [self.selenium.find_element_by_id('transaction_deleted_' + str(i))]
                self.search = self.selenium.find_element_by_xpath("//input[@type='search']")

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
            self.assertIn(str(transactions[i].transaction_wage), self.__get_text(page.wage[i]))
            self.assertIn(transactions[i].transaction_owner.username, self.__get_text(page.owner[i]))
            self.assertIn(transactions[i].transaction_status, self.__get_text(page.status[i]))
            self.assertIn(str(transactions[i].transaction_deleted), self.__get_text(page.deleted[i]))


