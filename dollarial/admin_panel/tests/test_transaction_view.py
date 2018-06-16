from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


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

                # self.banned = self.selenium.find_element_by_xpath("//input[@type='checkbox' and @id='cc-banned']")
                self.accept_button = self.selenium.find_element_by_xpath("//button[@type='button' and @class='btn "
                                                                         "btn-success btn-sm']")
                self.reject_button = self.selenium.find_element_by_xpath("//button[@type='submit' and @class='btn "
                                                                         "btn-danger btn-sm']")
                self.skip_button = self.selenium.find_element_by_xpath("//button[@type='reset' and @class='btn "
                                                                       "btn-secondary btn-sm']")
                self.report_button = self.selenium.find_element_by_xpath("//button[@type='submit' and @class='btn "
                                                                         "btn-warning btn-sm']")

            def accept(self):
                self.accept_button.click()

            def reject(self):
                self.reject_button.click()

            def report(self):
                self.report_button.click()

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

    # def test_fields_of_costumer(self):
    #     page = self.__get_page()
    #     costumer = self.__get_transaction()
    #     self.assertEqual(costumer.id, self.__get_value(page.id))
    #     self.assertEqual(costumer.type, self.__get_value(page.type))
    #     self.assertEqual(costumer.link, self.__get_value(page.link))
    #     self.assertEqual(costumer.amount, self.__get_value(page.amount))
    #     self.assertEqual(costumer.owner, self.__get_value(page.owner))
    #     self.assertEqual(costumer.destination, self.__get_value(page.destination))
    #     self.assertEqual(costumer.status, self.__get_checked(page.status))

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

    def test_report_button(self):
        pass
