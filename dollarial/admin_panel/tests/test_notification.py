from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class NotifTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/send_notification/'))

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()
        pass

    def __get_page(self):
        class NotifPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.disc= self.selenium.find_element_by_id('notification-text')
                self.button = self.selenium.find_element_by_css_selector("button.btn-primary")
                self.cancel_button = self.selenium.find_element_by_css_selector("button.btn-danger")
        return NotifPage(self.selenium)

    @staticmethod
    def _fill(page):
        page.disc.send_keys('Hey Whats Up')

    @staticmethod
    def _login(page): #TODO
        pass

    def test_not_loggedin(self): #TODO
        pass

    def test_successful_notif(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Notification Has Sent Successfully")

    def test_cancel_notif(self):
            page = self.__get_page()
            self._login(page)
            self._fill(page)
            page.cancel_button.click()
            success = self.selenium.find_element_by_css_selector('.success')
            self.assertEqual(success.text, "Canceled")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_add(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.disc]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

