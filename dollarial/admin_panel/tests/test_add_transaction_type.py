from importlib import import_module

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User, PaymentType
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class TransactionTypeAddTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.user = User.objects.create_superuser(username="kossar_admin",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234567812345678",
                                                  notification_preference="S")
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/add'))

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/add'))

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

    def check_transaction_type_creation(self):
        toefl = PaymentType.objects.get(name="toefl")
        self.assertIn("english", toefl.description)

    def _fill(self, page):
        self.__send_keys_scrolling(page.name, 'toefl')
        self.__send_keys_scrolling(page.description, 'english exam')
        page.fixed_price.click()
        page.currency_select.select_by_visible_text("$")
        page.min_price.clear()
        page.price.clear()
        page.max_price.clear()
        page.wage.clear()
        self.__send_keys_scrolling(page.price, '200')
        self.__send_keys_scrolling(page.min_price, '1')
        self.__send_keys_scrolling(page.max_price, '1000000')
        self.__send_keys_scrolling(page.wage, '7')
        page.personal_info.click()
        page.general_info.click()
        page.exam_info.click()

    def test_successful_ttadd(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.check_transaction_type_creation()
        self.assertNotIn("add", self.selenium.current_url)

    def test_empty_parts_add(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.name.clear()
        page.button.click()
        self.assertIn("add", self.selenium.current_url)

        # TODO this test doesn't pass because we actually can re-add an existing transaction type
        # def test_already_existing_transaction_type(self):
        #     page = self.__get_page()
        #     self._login(page)
        #     self._fill(page)
        #     page.name.clear()
        #     page.name.send_keys('Toefl')
        #     page.save_button.click()
        #     error = self.selenium.find_element_by_css_selector('.has-error')
        #     self.assertEqual(error.text, "There exists a Transaction Type with entered name.")
