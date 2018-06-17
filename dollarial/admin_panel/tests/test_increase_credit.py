from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class IncreaseCreditTestCase(StaticLiveServerTestCase):
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
    def _login(): #TODO
        pass

    def test_not_loggedin(self): #TODO
        pass

    def test_not_admin(self):  # TODO
        pass


    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/'))

    def __add_data(self):

        #todo add to db

        data = {
            "wallets": [
                {"name": "dollar",
                 "credit": 2200,
                 },
                {"name": "rial",
                 "credit": 1000,
                 },
                {"name": "euro",
                 "credit": 1020
                 }
            ]
        }
        return data

    def test_increase_successfully(self):
        self._login()
        data = self.__add_data()

        i = 0
        for d in data:
            amount = self.selenium.find_element_by_id("cc-price_" + str(i))
            charge = self.selenium.find_element_by_id("charge_" + str(i))
            amount.send_keys(1234)
            charge.click()
            time.sleep(1)
            confirm = self.selenium.find_element_by_css_selector("button.btn-primary")
            confirm.click()
            success = self.selenium.find_element_by_css_selector('.success')
            self.assertEqual(success.text, "Increased Successfully")
            break

    def test_increase_cancel(self):
        data = self.__add_data()

        i = 0
        for d in data:
            amount = self.selenium.find_element_by_id("cc-price_" + str(i))
            charge = self.selenium.find_element_by_id("charge_" + str(i))
            amount.send_keys(1234)
            charge.click()
            time.sleep(1)
            cancel = self.selenium.find_element_by_css_selector("button.btn-secondary")
            cancel.click()
            success = self.selenium.find_element_by_css_selector('.success')
            self.assertEqual(success.text, "Cancel")
            break


