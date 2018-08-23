from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        User.objects.create(username="test", password="kossarnajafi1")

    def __get_page(self):
        class LoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.password = self.selenium.find_element_by_id('id_password')
                # self.button = self.selenium.find_element_by_xpath("//button[@class='btn btn-primary']")
                self.button = WebDriverWait(self.selenium, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button"))
                )

        return LoginPage(self.selenium)

    # def test_successful_login(self):
    #     page = self.__get_page()
    #     page.password = WebDriverWait(self.selenium, 10).until(
    #         EC.presence_of_element_located((By.ID, "id_password"))
    #     )
    #     page.password.click()
    #     page.password.send_keys('kossarnajafi1')
    #     page.username = WebDriverWait(self.selenium, 10).until(
    #         EC.presence_of_element_located((By.ID, "id_username"))
    #     )
    #     page.username.send_keys('test')
    #
    #     page.button = WebDriverWait(self.selenium, 10).until(
    #         EC.presence_of_element_located((By.TAG_NAME, "button"))
    #     )
    #     page.button.click()
    #     # page.username.click()
    #     # self.selenium.implicitly_wait(30)
    #     # page.username.send_keys('after')
    #     # page.password.send_keys('afteriwenthomeistartedworking')
    #     _ = WebDriverWait(self.selenium, 10).until(
    #         EC.presence_of_element_located((By.ID, "logout"))
    #     )
    #     self.selenium.find_element_by_id('logout')

    def test_wrong_email_login(self):
        page = self.__get_page()
        page.username = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        page.username.send_keys('soroush1')
        page.password = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "id_password"))
        )
        page.password.send_keys('123')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')

    def test_wrong_password_login(self):
        page = self.__get_page()
        page.password = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "id_password"))
        )
        page.username.send_keys('soroush')
        page.password = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "id_password"))
        )
        page.password.send_keys('xxx')
        page.button.click()
        _ = self.selenium.find_element_by_class_name('alert-danger')
