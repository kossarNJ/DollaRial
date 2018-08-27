from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class CustomerBanTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/1'))

    def tearDown(self):
        self.selenium.quit()

    def __create_users(self):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/1'))

    def __get_page(self):
        class CustomerBanPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.first_name = self.selenium.find_element_by_id('id_first_name')
                self.last_name = self.selenium.find_element_by_id('id_last_name')
                self.account = self.selenium.find_element_by_id('id_account_number')
                self.email = self.selenium.find_element_by_id('id_email')
                self.phone = self.selenium.find_element_by_id('id_phone_number')
                self.active = self.selenium.find_element_by_id('id_is_active')
                self.staff = self.selenium.find_element_by_id('id_is_staff')

                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return CustomerBanPage(self.selenium)

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
    def __get_costumer():
        costumer = User.objects.get(id="1")
        return costumer

    def test_ban_button(self):
        self.__create_users()
        self.login()
        page = self.__get_page()
        page.active.click()
        page.button.click()
        active_status = self.__get_costumer().is_active
        self.assertIn("False", str(active_status))
