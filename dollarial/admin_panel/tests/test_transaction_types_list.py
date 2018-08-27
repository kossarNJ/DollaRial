from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User, PaymentType
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class TransactionListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_transaction_types()

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
        self.__create_transaction_types()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/'))

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/'))

    @staticmethod
    def __create_transaction_types():
        type1 = PaymentType(name="toefl", description="english exam", price="200", currency="$")
        type1.save()
        type2 = PaymentType(name="ielts", description="english exam", price="200", currency="$")
        type2.save()
        type3 = PaymentType(name="gre", description="english exam", price="200", currency="$")
        type3.save()

    def __get_transaction_types(self):
        class TransactionTypeItem(object):
            def __init__(self, transaction_id, transaction_name,
                         transaction_fixed_price, transaction_price, transaction_currency,
                         transaction_min, transaction_max, transaction_wage):
                self.transaction_id = transaction_id
                self.transaction_name = transaction_name
                self.transaction_fixed_price = transaction_fixed_price
                self.transaction_price = transaction_price
                self.transaction_currency = transaction_currency
                self.transaction_min = transaction_min
                self.transaction_max = transaction_max
                self.transaction_wage = transaction_wage

        transactions = PaymentType.objects.all()
        result = []
        for tr in transactions:
            result += [TransactionTypeItem(tr.id, tr.name, tr.fixed_price, tr.price,
                                           tr.currency, tr.min_amount, tr.max_amount, tr.wage_percentage)]
        return result

    def __get_page(self):
        class TransactionTypesListPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = []
                self.name = []
                self.fixed_price = []
                self.price = []
                self.currency = []
                self.min = []
                self.max = []
                self.wage = []

                for i in range(1, 4):
                    self.id += [self.selenium.find_element_by_id('type_id_' + str(i))]
                    self.name += [self.selenium.find_element_by_id('type_name_' + str(i))]
                    self.fixed_price += [self.selenium.find_element_by_id('type_fixed_price_' + str(i))]
                    self.price += [self.selenium.find_element_by_id('type_price_' + str(i))]
                    self.currency += [self.selenium.find_element_by_id('type_currency_' + str(i))]
                    self.min += [self.selenium.find_element_by_id('type_min_' + str(i))]
                    self.max += [self.selenium.find_element_by_id('type_max_' + str(i))]
                    self.wage += [self.selenium.find_element_by_id('type_wage_' + str(i))]

        return TransactionTypesListPage(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        self.login()
        transaction_types = self.__get_transaction_types()
        page = self.__get_page()
        for i in range(3):
            self.assertIn(str(transaction_types[i].transaction_id), self.__get_text(page.id[i]))
            self.assertIn(transaction_types[i].transaction_name, self.__get_text(page.name[i]))
            self.assertIn(str(transaction_types[i].transaction_fixed_price), self.__get_text(page.fixed_price[i]))
            self.assertIn(str(transaction_types[i].transaction_price), self.__get_text(page.price[i]))
            self.assertIn(transaction_types[i].transaction_currency, self.__get_text(page.currency[i]))
            self.assertIn(str(transaction_types[i].transaction_min), self.__get_text(page.min[i]))
            self.assertIn(str(transaction_types[i].transaction_max), self.__get_text(page.max[i]))
            self.assertIn(str(transaction_types[i].transaction_wage), self.__get_text(page.wage[i]))
