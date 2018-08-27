import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dollarial.models import User


class AdminLoginTest(StaticLiveServerTestCase):
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
        self.user = User.objects.create_superuser(username="kossar",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234432112344321",
                                                  notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/account/login/'))

    def __get_page(self):
        class AdminLoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.password = self.selenium.find_element_by_id('id_password')
                self.button = WebDriverWait(self.selenium, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button"))
                )

        return AdminLoginPage(self.selenium)

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def test_successful_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'kossar')
        self.__send_keys_scrolling(page.password, 'likeicare')
        page.button.click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.assertIn("user_panel", self.selenium.current_url)

    def test_wrong_username_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'kossar1')
        self.__send_keys_scrolling(page.password, 'likeicare')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')

    def test_wrong_password_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'kossar')
        self.__send_keys_scrolling(page.password, 'wrongpass')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')
