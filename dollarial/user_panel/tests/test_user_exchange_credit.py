from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class ExchangeCreditTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/exchange'))
        self.__create_users()

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()

    def __create_users(self):
        """
         TODO: add reviewers to database
         user1
         user2
         ...
        """
        pass

    def __get_page_1(self):
        class ExchangePage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.from_curr = Select(self.selenium.find_element_by_id('from-currency-select'))
                self.to_curr = Select(self.selenium.find_element_by_id('to-currency-select'))
                self.amount = self.selenium.find_element_by_id('amount')
                self.from_radio = self.selenium.find_element_by_xpath("//input[@type='radio' and @value='from']")
                self.to_radio = self.selenium.find_element_by_xpath("//input[@type='radio' and @value='to']")
                self.preview_button = self.selenium.find_element_by_id('preview_exchange')

        return ExchangePage(self.selenium)

    def __get_page_2(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/exchange/accept/'))

        class ExchangePreviewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.confirm_exchange = self.selenium.find_element_by_id('confirm-exchange')
                self.cancel_exchange = self.selenium.find_element_by_id('cancel-exchange')

        return ExchangePreviewPage(self.selenium)

    @staticmethod
    def _fill_1(page):
        page.amount.send_keys('100')
        page.to_radio.click()

        for option in page.from_curr.options:
            if option.text == 'Dollar':
                option.click()
                break
        for option in page.to_curr.options:
            if option.text == 'Euro':
                option.click()
                break

    @staticmethod
    def _login(page):  # TODO
        pass

    def test_not_logged_in(self):  # TODO
        pass

    def test_preview_exchange_not_empty(self):
        page = self.__get_page_1()
        self._login(page)
        self._fill_1(page)

        prev_text = self.__get_text(page.amount)
        page.amount.clear()
        page.preview_button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Please fill all required fields.")
        page.amount.send_keys(prev_text)

        page.from_curr.deselect_all()
        page.preview_button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Please fill all required fields.")
        for option in page.from_curr.options:
            if option.text == 'Dollar':
                option.click()
                break

        page.to_curr.deselect_all()
        page.preview_button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Please fill all required fields.")
        for option in page.to_curr.options:
            if option.text == 'Euro':
                option.click()
                break

        page.to_radio.click()
        page.preview_button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Please fill all required fields.")
        page.to_radio.click()

    def test_preview_exchange(self):
        page = self.__get_page_1()
        self._login(page)
        self._fill_1(page)
        page.preview_button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Exchange Successfully Submitted")

    def test_preview_accept(self):
        page1 = self.__get_page_1()
        self._login(page1)
        self._fill_1(page1)
        page1.preview_button.click()
        self.selenium.implicitly_wait(10)

        page2 = self.__get_page_2()
        page2.confirm_exchange.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Exchange Successfully Made")

    def test_preview_fail_unsuccessful(self):
        page1 = self.__get_page_1()
        self._login(page1)
        self._fill_1(page1)
        page1.amount.send_keys('10000000')
        page1.preview_button.click()
        self.selenium.implicitly_wait(10)

        page2 = self.__get_page_2()
        page2.confirm_exchange.click()
        error = self.selenium.find_element_by_css_selector('.error')
        self.assertEqual(error.text, "Exchange unsuccessful. You can not exchange more than ")

    def test_preview_accept_unsuccess(self):
        page1 = self.__get_page_1()
        self._login(page1)
        self._fill_1(page1)
        page1.amount.send_keys('100000')  # amount that is more than balance of account
        page1.preview_button.click()
        self.selenium.implicitly_wait(10)

        page2 = self.__get_page_2()
        page2.confirm_exchange.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "The amount is more than the current balance")

    def test_preview_cancel(self):
        page1 = self.__get_page_1()
        self._login(page1)
        self._fill_1(page1)
        page1.preview_button.click()
        self.selenium.implicitly_wait(10)

        page2 = self.__get_page_2()
        page2.cancel_exchange.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Exchange Canceled")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')
