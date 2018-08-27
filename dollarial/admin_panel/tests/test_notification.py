from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class NotifTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/send_notification/'))

    def tearDown(self):
        self.selenium.quit()

    def __get_page(self):
        class NotifPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.subject = self.selenium.find_element_by_id('id_subject')
                self.text = self.selenium.find_element_by_id("id_notification_text")
                buttons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
                self.send_button = buttons[0]
                self.cancel_button = buttons[1]

        return NotifPage(self.selenium)

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/send_notification/'))

    @staticmethod
    def _fill(page):
        page.subject.send_keys('HEllO')
        page.text.send_keys('Hi! Welcome to Dollarial')

    def test_successful_notif(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.send_button.click()
        self.assertNotIn("send_notification", self.selenium.current_url)

    def test_cancel_notif(self):
        self.login()
        page = self.__get_page()
        page.cancel_button.click()
        self.assertNotIn("send_notification", self.selenium.current_url)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_add(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.subject.clear()
        page.send_button.click()
        self.assertIn("send_notification", self.selenium.current_url)
