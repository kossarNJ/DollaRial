from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class RegistrationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/account/registration/'))
        self.__create_users()

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()
        pass

    def __create_users(self):
        # TODO: add user to database
        pass

    def __get_page(self):
        class RegistrationPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.email = self.selenium.find_element_by_id('email')
                self.password = self.selenium.find_element_by_id('pass')
                self.fname = self.selenium.find_element_by_id('fname')
                self.lname = self.selenium.find_element_by_id('lname')
                self.phone = self.selenium.find_element_by_id('telephone')
                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return RegistrationPage(self.selenium)

    def check_user_creation(self):
        # TODO: check user soroush creation
        pass

    @staticmethod
    def _fill(page):
        page.email.send_keys('soroush@divar.ir')
        page.password.send_keys('123')
        page.fname.send_keys('Soroush')
        page.lname.send_keys('Ebadian')
        page.phone.send_keys('09352543617')

    def test_successful_registration(self):
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        self.check_user_creation()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Hi Soroush!")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_registration(self):
        page = self.__get_page()
        fields = [page.fname, page.lname, page.password, page.email, page.phone]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

    def test_already_existing_user(self):
        page = self.__get_page()
        self._fill(page)
        page.email.clear()
        page.email.send_keys('dollarialsharif@gmail.com')
        page.button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "There exists an account with entered email.")
