from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class CostumerListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_costumers()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/'))

    @classmethod
    def __create_costumers(self):
        # TODO: insert customers to DB with fields of CostumerItem
        pass

    def __get_costumers(self):
        # TODO: get list of costumers from DB
        class CostumerItem(object):
            def __init__(self, costumer_id, costumer_fname, costumer_lname, costumer_account_number, costumer_email,
                         costumer_phone_number, costumer_ban_status):
                self.costumer_id = costumer_id
                self.costumer_fname = costumer_fname
                self.costumer_lname = costumer_lname
                self.costumer_account_number = costumer_account_number
                self.costumer_email = costumer_email
                self.costumer_phone_number = costumer_phone_number
                self.costumer_ban_status = costumer_ban_status

        return [CostumerItem("1", "soroush", "ebadian", "123456789123", "soroushebadian@gmail.com", "0989352543617",
                             "False"),
                CostumerItem("2", "soroush2", "ebadian", "1234567891232", "soro2ushebadian@gmail.com", "0989352523617",
                             "True")]

    def __get_page(self):
        class CostumerListPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.fname = []
                self.lname = []
                self.account_number = []
                self.email = []
                self.phone_number = []
                self.ban_status = []
                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('costumer_id_' + row.costumer_id)]
                    self.fname += [self.selenium.find_element_by_id('costumer_fname_' + row.costumer_id)]
                    self.lname += [self.selenium.find_element_by_id('costumer_lname_' + row.costumer_id)]
                    self.account_number += [self.selenium.find_element_by_id('costumer_account_number_' +
                                                                             row.costumer_id)]
                    self.email += [self.selenium.find_element_by_id('costumer_email_' + row.costumer_id)]
                    self.phone_number += [self.selenium.find_element_by_id('costumer_phone_number_' + row.costumer_id)]
                    self.ban_status += [self.selenium.find_element_by_id('costumer_ban_status_' + row.costumer_id)]

        return CostumerListPage(self.selenium, self.__get_costumers())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        costumers = self.__get_costumers()
        page = self.__get_page()
        i = 0
        for item in costumers:
            self.assertEqual(item.costumer_id, self.__get_text(page.id[i]))
            self.assertEqual(item.costumer_fname, self.__get_text(page.fname[i]))
            self.assertEqual(item.costumer_lname, self.__get_text(page.lname[i]))
            self.assertEqual(item.costumer_account_number, self.__get_text(page.account_number[i]))
            self.assertEqual(item.costumer_email, self.__get_text(page.email[i]))
            self.assertEqual(item.costumer_phone_number, self.__get_text(page.phone_number[i]))
            self.assertEqual(item.costumer_ban_status, self.__get_text(page.ban_status[i]))
            i += 1

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
