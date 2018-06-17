from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ReportsTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_reports()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reports/'))

    @classmethod
    def __create_reports(self):
        # TODO: insert reports to DB with fields of ReportItem
        pass

    def __get_reports(self):
        # TODO: get list of reports from DB
        class ReportItem(object):
            def __init__(self, report_id, reviewer_id, transaction_id, report_message):
                self.report_id = report_id
                self.reviewer_id = reviewer_id
                self.transaction_id = transaction_id
                self.report_message = report_message

        return [ReportItem("1", "100", "10", "ekhtelas"), ReportItem("2", "101", "11", "ekhtelas")]

    def __get_page(self):
        class ReportPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.reviewer_id = []
                self.transaction_id = []
                self.report_message = []
                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('report_id_' + row.report_id)]
                    self.reviewer_id += [self.selenium.find_element_by_id('reviewer_id_' + row.report_id)]
                    self.transaction_id += [self.selenium.find_element_by_id('transaction_id_' + row.report_id)]
                    self.report_message += [self.selenium.find_element_by_id('report_message_' + row.report_id)]

        return ReportPage(self.selenium, self.__get_reports())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        reports = self.__get_reports()
        page = self.__get_page()
        i = 0
        for item in reports:
            self.assertEqual(item.report_id, self.__get_text(page.id[i]))
            self.assertEqual(item.reviewer_id, self.__get_text(page.reviewer_id[i]))
            self.assertEqual(item.transaction_id, self.__get_text(page.transaction_id[i]))
            self.assertContains(item.report_message, self.__get_text(page.report_message[i]))
            i += 1

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
