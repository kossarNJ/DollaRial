from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time
class AdminLogoutTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/'))

    def tearDown(self):
        # TODO: drop database
        pass

    def __login(self):
        #TODO
        pass

    def __get_page(self):
        class AdminLogoutPage(object):
            def __init__(self, selenium):

                self.selenium = selenium
                self.userlogo = self.selenium.find_element_by_id("userlogo")
                self.button = self.selenium.find_element_by_id("logout")

        return AdminLogoutPage(self.selenium)

    def test_successful_logout(self):
        self.__login()
        page = self.__get_page()
        page.userlogo.click()
        time.sleep(1)
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Logged Out Successfully")


    def test_logged_in(self):
        #TODO
        pass