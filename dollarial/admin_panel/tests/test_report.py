from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ReportTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions/1'))

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()
        pass

    def __get_page(self):
        class ReportPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.comment= self.selenium.find_element_by_id('report-comment')
                self.button = self.selenium.find_element_by_css_selector("button.btn-warning")
        return ReportPage(self.selenium)

    @staticmethod
    def _fill(page):
        page.comment.send_keys('suspicious')

    @staticmethod
    def _login(page): #TODO
        pass

    def test_not_loggedin(self): #TODO
        pass

    def test_successful_report(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Reported Successfully")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_add(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.comment]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

