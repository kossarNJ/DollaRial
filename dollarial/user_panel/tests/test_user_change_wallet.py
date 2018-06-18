from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChangeWalletTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    def __get_page(self):
        class IndexPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.charge_amount = self.selenium.find_element_by_id('charge-price')
                self.charge_button = self.selenium.find_element_by_id('charge-button')
                self.withdraw_amount = self.selenium.find_element_by_id('withdraw-price')
                self.withdraw_button = self.selenium.find_element_by_id('withdraw-button')

                try:
                    self.confirm_withdraw = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "confirm-withdraw"))
                    )
                    self.cancel_withdraw = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "cancel-withdraw"))
                    )
                    self.confirm_charge = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "confirm-charge"))
                    )
                    self.cancel_charge = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "cancel-charge"))
                    )
                finally:
                    pass

        return IndexPage(self.selenium)

    @staticmethod
    def _login(page):  # TODO
        pass

    def test_not_loggedIn(self):  # TODO
        pass

    def test_not_user(self):  # TODO
        pass

    @staticmethod
    def _fill(page):
        page.charge_amount.clear()
        page.withdraw_amount.clear()
        page.charge_amount.send_keys('100')
        page.withdraw_amount.send_keys('200')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_charge_wallet_successful(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.charge_button.click()
        page.confirm_charge.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Wallet Successfully Charged")

    def test_charge_wallet_cancel(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.charge_button.click()
        page.cancel_charge.click()
        self.assertEqual(self.__get_text(page.charge_amount), "")

    def test_charge_wallet_unsuccessful(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.charge_amount.clear()
        page.charge_button.click()
        page.confirm_charge.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Wallet Charge Unsuccessful")

    def test_withdraw_wallet_successful(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.withdraw_button.click()
        page.confirm_withdraw.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Withdrawal from Wallet Successful")

    def test_withdraw_wallet_cancel(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.withdraw_button.click()
        page.cancel_withdraw.click()
        self.assertEqual(self.__get_text(page.withdraw_amount), "")

    def test_withdraw_wallet_unsuccessful(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.withdraw_amount.clear()
        page.withdraw_button.click()
        page.confirm_withdraw.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Withdrawal from Wallet Unsuccessful")


