from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.currency import get_dollar_rial_value
from dollarial.currency import get_euro_rial_value


class CurrencyTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.currencies = cls.__get_currencies()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @classmethod
    def __get_currencies(cls):
        class Currencies(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.dollarPrice = get_dollar_rial_value()
                self.euroPrice = get_euro_rial_value()

        return Currencies(cls.selenium)

    def test_currency(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/currencies/'))
        dollar = self.selenium.find_element_by_id("price_dollar")
        euro = self.selenium.find_element_by_id("price_euro")
        wage = self.selenium.find_element_by_id("price_wage")
        self.assertIn(str(self.currencies.dollarPrice) + " IRR", self.__get_text(dollar))
        self.assertIn(str(self.currencies.euroPrice) + " IRR", self.__get_text(euro))
        self.assertIn("7" + "%", self.__get_text(wage))

    def test_exchange(self):
        amount = self.selenium.find_element_by_id("amount")
        result = self.selenium.find_element_by_id("cc-amount")
        button = self.selenium.find_element_by_xpath("//button[@type='button']")

        select1 = Select(self.selenium.find_element_by_id('currency_1'))
        select1.select_by_visible_text('Dollar')

        select2 = Select(self.selenium.find_element_by_id('currency_2'))
        select2.select_by_visible_text('Rial')

        amount.send_keys(1)
        button.click()

        self.assertEqual(float(result.get_attribute("value")), self.currencies.dollarPrice)
