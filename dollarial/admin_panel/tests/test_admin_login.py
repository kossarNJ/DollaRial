from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


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

    def __create_users(self):
        # TODO: add employee to database
        pass

    def setUp(self):
        self.__create_users()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/login/'))

    def tearDown(self):
        # TODO: drop database
        pass

    def __get_page(self):
        class AdminLoginPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('username')
                self.password = self.selenium.find_element_by_id('pass')
                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return AdminLoginPage(self.selenium)

    def test_successful_login(self):
        page = self.__get_page()
        page.username.send_keys('parand@cafebazaar.ir')
        page.password.send_keys('12345')
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Hi Parand!")

    def test_wrong_username_login(self):
        page = self.__get_page()
        page.username.send_keys('parand')
        page.password.send_keys('12345')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Wrong username/password.")

    def test_wrong_password_login(self):
        page = self.__get_page()
        page.username.send_keys('parand@cafebazaar.ir')
        page.password.send_keys('xxx')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Wrong username/password.")
