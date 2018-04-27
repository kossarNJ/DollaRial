from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class LoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def __create_users(self):
        # TODO: add user to database
        pass

    def setUp(self):
        self.__create_users()
        self.selenium.get('%s%s' % (self.live_server_url, '/account/login/'))

    def tearDown(self):
        # TODO: drop database
        pass

    def __get_page(self):
        class LoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.email = self.selenium.find_element_by_id('email')
                self.password = self.selenium.find_element_by_id('pass')
                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return LoginPage(self.selenium)

    def test_successful_login(self):
        page = self.__get_page()
        page.email.send_keys('soroush@divar.ir')
        page.password.send_keys('123')
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Hi Soroush!")

    def test_wrong_email_login(self):
        page = self.__get_page()
        page.email.send_keys('soroush')
        page.password.send_keys('123')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Wrong email/password.")

    def test_wrong_password_login(self):
        page = self.__get_page()
        page.email.send_keys('soroush@divar.ir')
        page.password.send_keys('xxx')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Wrong email/password.")
