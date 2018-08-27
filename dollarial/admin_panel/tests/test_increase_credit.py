from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time

from selenium.webdriver.support.select import Select

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class IncreaseCreditTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def tearDown(self):
        self.selenium.quit()

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/charge/'))

    def setUp(self):
        self.user = User.objects.create_superuser(username="kossar_admin",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234567812345678",
                                                  notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/charge/'))

    def __get_page(self):
        class IncreaseCredit(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.amount = self.selenium.find_element_by_id('id_amount')
                self.currency = Select(self.selenium.find_element_by_id('id_currency'))
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return IncreaseCredit(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def check_wallet(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/'))
        dollar = self.selenium.find_element_by_xpath(
            '//*[@id="right-panel"]/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div[2]')
        self.assertIn("2000", self.__get_text(dollar))

    @staticmethod
    def _fill(page):
        page.amount.clear()
        page.amount.send_keys("2000")
        page.currency.select_by_visible_text("$")

    def test_increase_successfully(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.check_wallet()
        self.assertNotIn("charge", self.selenium.current_url)
