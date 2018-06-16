from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class RegistrationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))
        self.__create_users()

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()
        pass

    def __create_users(self):
        """
         TODO: add reviewers to database
         user1
         user2
         ...
        """
        pass

    def __get_page(self):
        class AddReviewerPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('cc-username')
                self.password = self.selenium.find_element_by_id('cc-password')
                self.salary = self.selenium.find_element_by_id('cc-salary')
                self.button = self.selenium.find_element_by_css_selector("button.btn-success")

        return AddReviewerPage(self.selenium)

    def check_user_creation(self):
        # TODO: check reviewer parand creation
        pass

    @staticmethod
    def _fill(page):
        page.username.send_keys('parand')
        page.password.send_keys('123')
        page.salary.send_keys('350000000')

    @staticmethod
    def _login(page): #TODO
        pass

    def test_not_loggedin(self): #TODO
        pass

    def test_successful_radd(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.button.click()
        self.check_user_creation()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "User Added Successfully")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_add(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.password, page.username, page.salary]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

    def test_already_existing_reviewer(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.username.clear()
        page.username.send_keys('admin')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "There exists an account with entered email.")
