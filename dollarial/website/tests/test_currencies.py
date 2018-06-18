from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class CurrencyTestCase(StaticLiveServerTestCase):
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



    def test_currency(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/currencies/'))

        dollar = self.selenium.find_element_by_id("price_dollar")
        euro = self.selenium.find_element_by_id("price_euro")
        wage = self.selenium.find_element_by_id("price_wage")
        self.assertIn("42000 IRR", self.__get_text(dollar))
        self.assertIn("53000 IRR", self.__get_text(euro))
        self.assertIn("7%", self.__get_text(wage))


    def test_exchange(self):
        currency1 = self.selenium.find_element_by_id("currency_1")
        currency2 = self.selenium.find_element_by_id("currency_2")
        amount = self.selenium.find_element_by_id("amount")
        result = self.selenium.find_element_by_id("cc-amount")

        for option in currency1.find_elements_by_tag_name('option'):
            if option.text == 'dollar':
                option.click()
                break

        for option in currency2.find_elements_by_tag_name('option'):
            if option.text == 'rial':
                option.click()
                break
        amount.send_keys('1')

        self.assertEqual(result.get_attribute("value"), '42000')



