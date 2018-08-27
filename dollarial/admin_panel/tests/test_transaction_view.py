from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.webdriver import WebDriver
from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings

from finance.models import Transaction


class TransactionViewTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def tearDown(self):
        self.selenium.quit()

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))

    def __get_page(self):
        class TransactionViewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                try:
                    self.accept_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_accept"))
                    )
                    self.reject_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_reject"))
                    )
                    self.skip_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_skip"))
                    )
                finally:
                    pass

                self.owner = self.selenium.find_element_by_id('cc-Owner')
                self.amount = self.selenium.find_element_by_id('cc-Amount')
                self.wage = self.selenium.find_element_by_id('cc-Wage')
                self.deleted = self.selenium.find_element_by_id('cc-Deleted')
                self.status = self.selenium.find_element_by_id('cc-Status')

            def accept(self):
                self.accept_button.click()

            def reject(self):
                self.reject_button.click()

            def skip(self):
                self.skip_button.click()

        return TransactionViewPage(self.selenium)

    @staticmethod
    def __get_value(element):
        return element.get_attribute('value')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    @staticmethod
    def __get_transaction():
        # TODO: pull soroush's changes and fix the last three tests
        transaction = Transaction.objects.get(id="1")
        return transaction

    def test_fields_of_costumer(self):
        self.login()
        page = self.__get_page()
        transaction = self.__get_transaction()
        self.assertIn(transaction.owner.username, self.__get_value(page.owner))
        self.assertIn(str(transaction.amount), self.__get_value(page.amount))
        self.assertIn(str(transaction.wage), self.__get_value(page.wage))
        self.assertIn(str(transaction.deleted), self.__get_value(page.deleted))
        self.assertIn(transaction.status, self.__get_value(page.status))

    # def test_accept_button(self):
    #     page = self.__get_page()
    #     page.accept()
    #     success = self.selenium.find_element_by_css_selector('.success')
    #     self.assertEqual(success.text, "Transaction has been accepted.")
    #
    # def test_reject_button(self):
    #     page = self.__get_page()
    #     page.reject()
    #     success = self.selenium.find_element_by_css_selector('.success')
    #     self.assertEqual(success.text, "Transaction has been rejected.")
    #
    # def test_skip_button(self):
    #     page = self.__get_page()
    #     page.skip()
    #     success = self.selenium.find_element_by_css_selector('.success')
    #     self.assertEqual(success.text, "Transaction has been skipped.")
