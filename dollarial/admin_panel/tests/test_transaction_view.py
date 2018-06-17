from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TransactionViewTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))

    def __get_page(self):
        class TransactionViewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = self.selenium.find_element_by_id('cc-id')
                self.type = self.selenium.find_element_by_id('cc-type')
                self.link = self.selenium.find_element_by_id('link_of_type')
                self.amount = self.selenium.find_element_by_id('cc-amount')
                self.owner = self.selenium.find_element_by_id('cc-owner')
                self.destination = self.selenium.find_element_by_id('cc-destination')
                self.status = self.selenium.find_element_by_id('cc-status')

                try:
                    self.accept_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_accept"))
                    )
                    self.reject_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_reject"))
                    )
                    self.skip_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "transaction_skip"))
                    )
                finally:
                    pass

            def accept(self):
                self.accept_button.click()

            def reject(self):
                self.reject_button.click()

            def skip(self):
                self.skip_button.click()

        return TransactionViewPage(self.selenium)

    @staticmethod
    def __get_value(element):
        return element.get_attribute('value')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    def __get_transaction(self):
        # TODO: get user from DB
        class Costumer(object):
            def __init__(self):
                self.id = " "
                self.type = " "
                self.link = " "
                self.amount = " "
                self.owner = " "
                self.destination = " "
                self.status = " "

        return Costumer()

    def test_fields_of_costumer(self):
        page = self.__get_page()
        costumer = self.__get_transaction()
        self.assertEqual(costumer.id, self.__get_value(page.id))
        self.assertEqual(costumer.type, self.__get_value(page.type))
        self.assertEqual(costumer.link, self.__get_value(page.link))
        self.assertEqual(costumer.amount, self.__get_value(page.amount))
        self.assertEqual(costumer.owner, self.__get_value(page.owner))
        self.assertEqual(costumer.destination, self.__get_value(page.destination))
        self.assertEqual(costumer.status, self.__get_checked(page.status))

    def test_accept_button(self):
        page = self.__get_page()
        page.accept()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Transaction has been accepted.")  # TODO: update this if necessary

    def test_reject_button(self):
        page = self.__get_page()
        page.reject()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Transaction has been rejected.")  # TODO: update this if necessary

    def test_skip_button(self):
        page = self.__get_page()
        page.skip()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Transaction has been skipped.")  # TODO: update this if necessary

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_clerk user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Clerk user should be able to access this page.
        pass
