from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User


class LoginTest(StaticLiveServerTestCase):
    def setUp(self):
        self.__create_users()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/account/login/'))

    def tearDown(self):
        self.selenium.quit()

    @staticmethod
    def __create_users():
        User.objects.create(username="soroush", password="123")

    def __get_page(self):
        class LoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.password = self.selenium.find_element_by_id('id_password')
                self.button = self.selenium.find_element_by_xpath("//button[@class='btn btn-primary']")

        return LoginPage(self.selenium)

    def test_successful_login(self):
        page = self.__get_page()
        page.username.send_keys('soroush')
        page.password.send_keys('123')
        page.button.click()

        _ = self.selenium.find_element_by_id('logout')

    def test_wrong_email_login(self):
        page = self.__get_page()
        page.username.send_keys('soroush1')
        page.password.send_keys('123')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')

    def test_wrong_password_login(self):
        page = self.__get_page()
        page.username.send_keys('soroush')
        page.password.send_keys('xxx')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')
