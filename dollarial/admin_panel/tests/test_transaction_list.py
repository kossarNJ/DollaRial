from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class TransactionListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_transactions()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/'))

    @classmethod
    def __create_transactions(self):
        # TODO: insert transactions to DB with fields of TransactionItem
        pass

    def __get_transaction(self):
        # TODO: get list of transactions from DB
        class TransactionItem(object):
            def __init__(self, transaction_id, transaction_type, transaction_amount, transaction_currency,
                         transaction_owner, transaction_destination, transaction_status):
                self.transaction_id = transaction_id
                self.transaction_type = transaction_type
                self.transaction_amount = transaction_amount
                self.transaction_currency = transaction_currency
                self.transaction_owner = transaction_owner
                self.transaction_destination = transaction_destination
                self.transaction_status = transaction_status

        return [TransactionItem("1", "Toefl", "200", "$", "user1", "Toefl Co.", "reject"),
                TransactionItem("2", "Gaj", "20000000000", "﷼", "user2", "Gaj Co.", "unknown"),
                TransactionItem("3", "IELTS", "100", "€", "user1", "Soroush Co.", "accept"),
                TransactionItem("4", "Toefl", "200", "$", "user2", "Toefl Co.", "reject")]

    def __get_page(self):
        class TransactionListPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.type = []
                self.amount = []
                self.currency = []
                self.owner = []
                self.destination = []
                self.status = []
                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('transaction_id_' + row.transaction_id)]
                    self.type += [self.selenium.find_element_by_id('transaction_type_' + row.transaction_id)]
                    self.amount += [self.selenium.find_element_by_id('transaction_amount_' + row.transaction_id)]
                    self.currency += [self.selenium.find_element_by_id('transaction_currency_' + row.transaction_id)]
                    self.owner += [self.selenium.find_element_by_id('transaction_owner_' + row.transaction_id)]
                    self.destination += [self.selenium.find_element_by_id('transaction_destination_' + row.transaction_id)]
                    self.status += [self.selenium.find_element_by_id('transaction_status_' + row.transaction_id)]

        return TransactionListPage(self.selenium, self.__get_transaction())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        transactions = self.__get_transaction()
        page = self.__get_page()
        i = 0
        for item in transactions:
            self.assertEqual(item.transaction_id, self.__get_text(page.id[i]))
            self.assertEqual(item.transaction_type, self.__get_text(page.type[i]))
            self.assertEqual(item.transaction_amount, self.__get_text(page.amount[i]))
            self.assertEqual(item.transaction_currency, self.__get_text(page.currency[i]))
            self.assertEqual(item.transaction_owner, self.__get_text(page.owner[i]))
            self.assertEqual(item.transaction_destination, self.__get_text(page.destination[i]))
            self.assertEqual(item.transaction_status, self.__get_text(page.status[i]))
            i += 1

    def test_not_logged_in_clerk_access(self):
        # TODO: implement. Non_clerk user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Clerk user should be able to access this page.
        pass
