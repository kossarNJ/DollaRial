from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/transactions/1'))

    @staticmethod
    def __create_transactions():
        user = User.objects.get(username="kossar")
        transaction1 = Transaction(owner=user, amount="300", currency="D")
        transaction1.save()

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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/transactions/1'))

    def __get_page(self):
        class TransactionViewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.owner = self.selenium.find_element_by_id('cc-Owner')
                self.amount = self.selenium.find_element_by_id('cc-Amount')
                self.wage = self.selenium.find_element_by_id('cc-Wage')
                self.deleted = self.selenium.find_element_by_id('cc-Deleted')
                self.status = self.selenium.find_element_by_id('cc-Status')

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

    def test_fields_of_costumer(self):
        self.login()
        self.__create_transactions()
        page = self.__get_page()
        self.transaction = Transaction.objects.get(id=1)
        self.assertIn(self.transaction.owner.username, self.__get_value(page.owner))
        self.assertIn(str(self.transaction.amount), self.__get_value(page.amount))
        self.assertIn(str(self.transaction.wage), self.__get_value(page.wage))
        self.assertIn(str(self.transaction.deleted), self.__get_value(page.deleted))
        self.assertIn(self.transaction.status, self.__get_value(page.status))
