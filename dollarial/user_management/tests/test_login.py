import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest(StaticLiveServerTestCase):
    fixtures = ['user_testdata.json']

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/account/login/'))

    def tearDown(self):
        self.selenium.quit()

    def __get_page(self):
        class LoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.password = self.selenium.find_element_by_id('id_password')
                self.button = WebDriverWait(self.selenium, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button"))
                )

        return LoginPage(self.selenium)

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def test_successful_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'test')
        self.__send_keys_scrolling(page.password, 'kossarnajafi1')
        page.button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "button"))
        )
        page.button.click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element_by_tag_name('body'))

    def test_wrong_email_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'soroush1')
        self.__send_keys_scrolling(page.password, '123')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')

    def test_wrong_password_login(self):
        page = self.__get_page()
        self.__send_keys_scrolling(page.username, 'soroush')
        self.__send_keys_scrolling(page.password, 'xxx')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')
