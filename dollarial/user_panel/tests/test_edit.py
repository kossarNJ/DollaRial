import time
from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class EditTest(StaticLiveServerTestCase):
    fixtures = ['user_panel_data.json']

    def setUp(self):
        self.selenium = WebDriver()
        self.user = User.objects.create_user(username="kossar",
                                             email="k_na@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/profile/'))

    def tearDown(self):
        self.selenium.quit()

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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/profile/'))

    def __get_page(self):
        class EditPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.email = self.selenium.find_element_by_id('id_email')
                self.fname = self.selenium.find_element_by_id('id_first_name')
                self.lname = self.selenium.find_element_by_id('id_last_name')
                self.phone = self.selenium.find_element_by_id('id_phone_number')
                self.notification = Select(self.selenium.find_element_by_id('id_notification_preference'))
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return EditPage(self.selenium)

    @staticmethod
    def _fill(page):
        page.username.clear()
        page.email.clear()
        page.fname.clear()
        page.lname.clear()
        page.phone.clear()

        page.username.send_keys('parand')
        page.email.send_keys('parand1997@gmail.com')
        page.fname.send_keys('Parand')
        page.lname.send_keys('Alizadeh')
        page.phone.send_keys('02347898557')
        page.notification.select_by_visible_text('sms')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def test_empty_parts_edit(self):
        self.login()
        page = self.__get_page()
        username = page.username
        username.clear()
        button = page.button
        button.click()
        success_set = self.selenium.find_elements_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertEqual(len(success_set), 0)

    def test_successful_edit(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        success = self.selenium.find_element_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertIn("Profile successfully updated!", self.__get_text(success))
