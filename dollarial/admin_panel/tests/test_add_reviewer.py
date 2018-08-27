from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class RegistrationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.__create_users()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))

    def tearDown(self):
        self.selenium.quit()
        pass

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))

    def __get_page(self):
        class AddReviewerPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = Select(self.selenium.find_element_by_id('id_user'))
                self.salary = self.selenium.find_element_by_id('id_salary')
                self.employee = self.selenium.find_element_by_id('id_is_employee')
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return AddReviewerPage(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def _fill(page):
        page.username.select_by_visible_text('kossar')
        page.salary.clear()
        page.salary.send_keys("2000")

    def test_successful_radd(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.assertNotIn("add", self.selenium.current_url)

    def test_empty_parts_add(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.username.select_by_visible_text("---------")
        page.button.click()
        self.assertIn("add", self.selenium.current_url)

    def test_already_existing_reviewer(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.assertIn("add", self.selenium.current_url)
