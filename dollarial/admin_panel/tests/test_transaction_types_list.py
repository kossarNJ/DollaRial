from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class TransactionListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_transaction_types()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/'))

    @classmethod
    def __create_transaction_types(self):
        # TODO: insert transition types to DB with fields of TransactionTypeItem
        pass

    def __get_transaction_types(self):
        # TODO: get list of transaction types from DB
        class TransactionTypeItem(object):
            def __init__(self, transaction_id, transaction_name, transaction_fixed, transaction_price, transaction_currency, transaction_min, transaction_max, transaction_wage):
                self.transaction_id = transaction_id
                self.transaction_name = transaction_name
                self.transaction_fixed_price = transaction_fixed
                self.transaction_price = transaction_price
                self.transaction_currency = transaction_currency
                self.transaction_min = transaction_min
                self.transaction_max = transaction_max
                self.transaction_wage = transaction_wage

        return [TransactionTypeItem("1", "Toefl", "true", "200", "$", "1000", "2000", "10"),
                TransactionTypeItem("2", "IELTS", "true", "200", "$", "None", "None", "10"),
                TransactionTypeItem("3", "Europe University", "false", "None", "€", "1000", "2000", "10"),
                TransactionTypeItem("4", "America University", "false", "None", "$", "1000", "2000", "10")]

    def __get_page(self):
        class TransactionTypesListPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.name = []
                self.fixed_price = []
                self.price = []
                self.currency = []
                self.min = []
                self.max = []
                self.wage = []

                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('type_id_' + row.transaction_id)]
                    self.name += [self.selenium.find_element_by_id('type_name_' + row.transaction_id)]
                    self.fixed_price += [self.selenium.find_element_by_id('type_fixed_price_' + row.transaction_id)]
                    self.price += [self.selenium.find_element_by_id('type_price_' + row.transaction_id)]
                    self.currency += [self.selenium.find_element_by_id('type_currency_' + row.transaction_id)]
                    self.min += [self.selenium.find_element_by_id('type_min_' + row.transaction_id)]
                    self.max += [self.selenium.find_element_by_id('type_max_' + row.transaction_id)]
                    self.wage += [self.selenium.find_element_by_id('type_wage_' + row.transaction_id)]

        return TransactionTypesListPage(self.selenium, self.__get_transaction_types())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        transaction_types = self.__get_transaction_types()
        page = self.__get_page()
        i = 0
        for item in transaction_types:
            self.assertEqual(item.transaction_id, self.__get_text(page.id[i]))
            self.assertEqual(item.transaction_name, self.__get_text(page.name[i]))
            self.assertEqual(item.transaction_fixed_price, self.__get_text(page.fixed_price[i]))
            self.assertEqual(item.transaction_price, self.__get_text(page.price[i]))
            self.assertEqual(item.transaction_currency, self.__get_text(page.currency[i]))
            self.assertEqual(item.transaction_min, self.__get_text(page.min[i]))
            self.assertEqual(item.transaction_max, self.__get_text(page.max[i]))
            self.assertEqual(item.transaction_wage, self.__get_text(page.wage[i]))
            i += 1

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
