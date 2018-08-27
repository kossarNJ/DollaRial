from importlib import import_module

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings

from finance.models import Transaction


class ReportTest(StaticLiveServerTestCase):
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
        self.user = User.objects.create_user(username="kossar",
                                             email="k_naa@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.__create_transactions()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))

    def tearDown(self):
        self.selenium.quit()

    @staticmethod
    def __create_transactions():
        user_k = User.objects.get(username="kossar")
        transaction1 = Transaction(owner=user_k, amount="300", currency="D")
        transaction1.save()

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
        class ReportPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.comment = self.selenium.find_element_by_id('id_comment')
                self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return ReportPage(self.selenium)

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def _fill(self, page):
        self.__send_keys_scrolling(page.comment, 'suspicious')

    def test_successful_report(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))
        p = self.selenium.find_elements_by_tag_name('p')
        self.assertEqual(len(p), 0)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

