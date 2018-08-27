from importlib import import_module

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User, PaymentType
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class TransactionTypeViewTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.user = User.objects.create_superuser(username="kossar_admin",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234567812345678",
                                                  notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/1'))

    def tearDown(self):
        self.selenium.quit()

    def __get_page(self):
        class TransactionTypeAddPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.name = self.selenium.find_element_by_id('id_name')
                self.description = self.selenium.find_element_by_id('id_description')
                self.fixed_price = self.selenium.find_element_by_id('id_fixed_price')
                self.currency_select = Select(self.selenium.find_element_by_id('id_currency'))
                self.price = self.selenium.find_element_by_id('id_price')
                self.min_price = self.selenium.find_element_by_id('id_min_amount')
                self.max_price = self.selenium.find_element_by_id('id_max_amount')
                self.wage = self.selenium.find_element_by_id('id_wage_percentage')
                # self.group = self.selenium.find_element_by_id('id_transaction_group')
                self.general_info = self.selenium.find_element_by_id('id_required_fields_0')
                self.personal_info = self.selenium.find_element_by_id('id_required_fields_1')
                self.exam_info = self.selenium.find_element_by_id('id_required_fields_2')
                self.university_info = self.selenium.find_element_by_id('id_required_fields_3')
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return TransactionTypeAddPage(self.selenium)

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/1'))

    @staticmethod
    def __create_transaction_types():
        type1 = PaymentType(name="toefl", description="english exam", price="200", currency="$")
        type1.save()
        type2 = PaymentType(name="ielts", description="english exam", price="200", currency="$")
        type2.save()
        type3 = PaymentType(name="gre", description="english exam", price="200", currency="$")
        type3.save()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def check_transaction_type_edit(self):
        toefl = PaymentType.objects.get(id="1")
        self.assertIn("This is an international exam evaluating", toefl.description)

    def test_successful_ttedit(self):
        self.__create_transaction_types()
        self.login()
        page = self.__get_page()
        page.description.clear()
        page.description.send_keys('This is an international exam evaluating one\'s aptitude in the English language.')
        page.button.click()
        self.check_transaction_type_edit()
        self.assertNotIn("add", self.selenium.current_url)

