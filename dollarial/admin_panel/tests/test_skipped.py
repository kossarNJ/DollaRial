from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from selenium.common.exceptions import StaleElementReferenceException


class SkippedTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_skipped_transactions()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/skipped/'))

    @classmethod
    def __create_skipped_transactions(self):
        # TODO: insert skipped transactions to DB with fields of SkippedItem
        pass

    def __get_skipped(self):
        # TODO: get list of skipped transactions from DB
        class SkippedItem(object):
            def __init__(self, item_id, reviewer_id, reviewer_username, transaction_id, review_time):
                self.item_id = item_id
                self.reviewer_id = reviewer_id
                self.reviewer_username = reviewer_username
                self.transaction_id = transaction_id
                self.review_time = review_time

        return [SkippedItem("1", "2", "soroush", "10", "01/01/99"), SkippedItem("2", "1", "parand", "9", "01/01/99")]

    def __get_page(self):
        class SkippedPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.reviewer_id = []
                self.reviewer_username = []
                self.transaction_id = []
                self.review_time = []
                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('item_id_'+row.item_id)]
                    self.reviewer_id += [self.selenium.find_element_by_id('item_reviewer_id_'+row.item_id)]
                    self.reviewer_username += [self.selenium.find_element_by_id('item_reviewer_username_'+row.item_id)]
                    self.transaction_id += [self.selenium.find_element_by_id('item_transaction_id_'+row.item_id)]
                    self.review_time += [self.selenium.find_element_by_id('item_time_'+row.item_id)]
                self.search = self.selenium.find_element_by_xpath("//input[@type='search']")

        return SkippedPage(self.selenium, self.__get_skipped())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_filter_by_reviewer(self):
        page = self.__get_page()
        page.search.send_keys("parand")
        sleep(10)
        for reviewer in page.reviewer_username:
            try:
                self.assertEqual(self.__get_text(reviewer), "parand")
                break
            except StaleElementReferenceException:
                pass

    def test_fields_content(self):
        skipped_transactions = self.__get_skipped()
        page = self.__get_page()
        i = 0
        for item in skipped_transactions:
            self.assertEqual(item.item_id, self.__get_text(page.id[i]))
            self.assertEqual(item.reviewer_id, self.__get_text(page.reviewer_id[i]))
            self.assertEqual(item.reviewer_username, self.__get_text(page.reviewer_username[i]))
            self.assertEqual(item.transaction_id, self.__get_text(page.transaction_id[i]))
            self.assertEqual(item.review_time, self.__get_text(page.review_time[i]))
            i += 1

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
