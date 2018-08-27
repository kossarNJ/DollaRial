from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class UserLogoutTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    def __get_page(self):
        class UserLogoutPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.user_logo = self.selenium.find_element_by_id("userlogo")
                self.button = self.selenium.find_element_by_id("logout")

        return UserLogoutPage(self.selenium)

    def test_successful_logout(self):
        self.login()
        page = self.__get_page()
        page.user_logo.click()
        time.sleep(1)
        page.button.click()
        self.assertIn("home", self.selenium.current_url)
