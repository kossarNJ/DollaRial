from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from dollarial.models import User


class RegistrationTest(StaticLiveServerTestCase):
    fixtures = ['user_testdata.json']

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/account/registration/'))

    def tearDown(self):
        self.selenium.quit()
        pass

    def __get_page(self):
        class RegistrationPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.username = self.selenium.find_element_by_id('id_username')
                self.first_name = self.selenium.find_element_by_id('id_first_name')
                self.last_name = self.selenium.find_element_by_id('id_last_name')
                self.email = self.selenium.find_element_by_id('id_email')
                self.phone_number = self.selenium.find_element_by_id('id_phone_number')
                self.password1 = self.selenium.find_element_by_id('id_password1')
                self.password2 = self.selenium.find_element_by_id('id_password2')
                self.account_number = self.selenium.find_element_by_id('id_account_number')
                self.notification = Select(self.selenium.find_element_by_id('id_notification_preference'))
                self.button = self.selenium.find_element_by_xpath("//button[@class='btn btn-primary']")

        return RegistrationPage(self.selenium)

    def check_user_creation(self):
        entries = User.objects.filter(first_name="soroush")
        self.assertEqual(entries[0].last_name, "ebadian")

    @staticmethod
    def _fill(page):
        page.username.send_keys('soroush_divar')
        page.first_name.send_keys('soroush')
        page.last_name.send_keys('ebadian')
        page.email.send_keys('soroush@divar.ir')
        page.phone_number.send_keys('09147898557')
        page.password1.send_keys('ihatemakinguppasswords')
        page.password2.send_keys('ihatemakinguppasswords')
        page.account_number.send_keys('5678123456781234')
        page.notification.select_by_visible_text('sms')

    def test_successful_registration(self):
        page = self.__get_page()
        self._fill(page)
        page.button.click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.check_user_creation()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_registration(self):
        page = self.__get_page()
        fields = [page.username, page.password1, page.password2, page.account_number]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            _ = self.selenium.find_element_by_id("id_phone_number")
            field.send_keys(prev_text)

    def test_already_existing_user(self):
        page = self.__get_page()
        self._fill(page)
        page.username.clear()
        page.username.send_keys('test')
        page.button.click()
        error = self.selenium.find_elements_by_tag_name('span')
        self.assertEqual(self.__get_text(error[0]), "A user with that username already exists.")
