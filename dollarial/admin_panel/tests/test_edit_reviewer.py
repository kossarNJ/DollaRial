from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class EditReviewerTestCase(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/1'))


    def __get_page(self):
        class EditPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id= self.selenium.find_element_by_id('cc-id')
                self.username= self.selenium.find_element_by_id('cc-username')
                self.salary= self.selenium.find_element_by_id('cc-salary')
                self.button = self.selenium.find_element_by_css_selector("button.btn-primary")
                self.password = self.selenium.find_element_by_id("password")
                self.repassword = self.selenium.find_element_by_id("re_password")
                self.savebutt = self.selenium.find_element_by_css_selector("button.btn-success")

        return EditPage(self.selenium)


    @staticmethod
    def _login(page): #TODO
        pass


    @staticmethod
    def _fill(page):
        page.id.clear()
        page.username.clear()
        page.salary.clear()
        page.id.send_keys('10')
        page.username.send_keys('parand_a')
        page.salary.send_keys('34666666')

    def test_edit_password_successfully(self):
        page = self.__get_page()
        self._login(page)
        page.password.send_keys("123")
        page.repassword.send_keys("123")
        page.savebutt.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Password Edited Successfully")

    def test_edit_successfully(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Edited Successfully")

    def test_empty_pass(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.password, page.repassword]
        page.password.send_keys("123")
        page.repassword.send_keys("123")
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.savebutt.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

    def test_not_matching_pass(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.password, page.repassword]
        page.password.send_keys("123")
        page.repassword.send_keys("143")

        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "password and its repeat don't match.")


    def test_not_loggedin(self): #TODO
        pass

    def test_not_admin(self):  # TODO
        pass

