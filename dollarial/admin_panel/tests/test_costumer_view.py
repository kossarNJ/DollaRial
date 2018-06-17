from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CustomerViewTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/1'))

    def __get_page(self):
        class CustomerViewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = self.selenium.find_element_by_id('cc-id')
                self.fname = self.selenium.find_element_by_id('cc-fname')
                self.lname = self.selenium.find_element_by_id('cc-lname')
                self.account = self.selenium.find_element_by_id('cc-account')
                self.email = self.selenium.find_element_by_id('cc-email')
                self.phone = self.selenium.find_element_by_id('cc-phone')
                self.banned = self.selenium.find_element_by_xpath("//input[@type='checkbox' and @id='cc-banned']")

                try:
                    self.confirm_ban_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "confirm_ban_button"))
                    )
                    self.cancel_ban_button = WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located((By.ID, "cancel_ban_button"))
                    )
                finally:
                    pass

                self.ban_button = self.selenium.find_element_by_xpath("//button[@type='button' and @class='btn "
                                                                      "btn-danger btn-sm']")
                self.save_button = self.selenium.find_element_by_xpath("//button[@type='submit' and @class='btn "
                                                                       "btn-primary btn-sm']")

            def save(self):
                self.save_button.click()

            def ban_costumer(self):
                self.ban_button.click()

            def confirm_ban(self):
                self.confirm_ban_button.click()

            def cancel_ban(self):
                self.cancel_ban_button.click()

        return CustomerViewPage(self.selenium)

    @staticmethod
    def __get_value(element):
        return element.get_attribute('value')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    def __get_costumer(self):
        # TODO: get user from DB
        class Costumer(object):
            def __init__(self):
                self.id = " "
                self.fname = " "
                self.lname = " "
                self.account = " "
                self.email = " "
                self.phone = " "
                self.banned_status = "true"

        return Costumer()

    def test_fields_of_costumer(self):
        page = self.__get_page()
        costumer = self.__get_costumer()
        self.assertEqual(costumer.id, self.__get_value(page.id))
        self.assertEqual(costumer.fname, self.__get_value(page.fname))
        self.assertEqual(costumer.lname, self.__get_value(page.lname))
        self.assertEqual(costumer.account, self.__get_value(page.account))
        self.assertEqual(costumer.email, self.__get_value(page.email))
        self.assertEqual(costumer.phone, self.__get_value(page.phone))
        self.assertEqual(costumer.banned_status, self.__get_checked(page.banned))

    def test_save_button(self):
        page = self.__get_page()
        page.save()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Changes have been saved.")  # TODO: update this if necessary

    def test_ban_button(self):
        page = self.__get_page()
        page.ban_costumer()
        if self.__get_checked(page.banned) is "false":
            self.assertEqual("Ban User", self.__get_text(page.banned))
            page.confirm_ban()
            success = self.selenium.find_element_by_css_selector('.success')
            self.assertEqual(success.text, "Costumer has been banned.")  # TODO: update this if necessary
            self.assertEqual("true", self.__get_checked(page.banned))
            self.assertEqual("Lift Ban", self.__get_text(page.banned))
        else:
            self.assertEqual("Lift Ban", self.__get_text(page.banned))
            page.confirm_ban()
            success = self.selenium.find_element_by_css_selector('.success')
            self.assertEqual(success.text, "Costumer's ban has been lifted.")  # TODO: update this if necessary
            self.assertEqual("false", self.__get_checked(page.banned))
            self.assertEqual("Ban User", self.__get_text(page.banned))

    def test_ban_button_cancel(self):
        page = self.__get_page()
        page.ban_costumer()
        if self.__get_checked(page.banned) is "false":
            self.assertEqual("Ban User", self.__get_text(page.banned))
            page.cancel_ban()
            self.assertEqual("false", self.__get_checked(page.banned))
            self.assertEqual("Ban User", self.__get_text(page.banned))
        else:
            self.assertEqual("Lift Ban", self.__get_text(page.banned))
            page.cancel_ban()
            self.assertEqual("true", self.__get_checked(page.banned))
            self.assertEqual("Lift Ban", self.__get_text(page.banned))

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
