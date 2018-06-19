from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time
class UserWalletsTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    def tearDown(self):
        # TODO: drop database
        pass

    def __login(self):
        # TODO
        pass

    def __add_data(self):
        #TODO db
        wallets =  [
            {"name": "rial",
             "credit": 1000,
             },
            {"name": "dollar",
             "credit": 2200,
             },
            {"name": "euro",
             "credit": 1020
             }
        ]
        return wallets

    def test_view_wallets(self):
        self.__login()
        data = self.__add_data()
        for d in data:
            credit = self.selenium.find_element_by_id("wallet_balance_" + d["name"])
            self.assertEqual(str(d["credit"]), self.__get_text(credit))


    def test_logged_in(self):
        #TODO
        pass