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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/transactions/1'))

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


    def test_logged_in_user_access(self):
        # TODO: implement.  user should be able to access this page.
        pass
