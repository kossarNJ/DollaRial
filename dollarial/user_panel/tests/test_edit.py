from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class EditTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/profile/'))
        self.__create_users()

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()
        pass

    def __create_users(self):
        # TODO: add user to database
        pass

    def __get_page(self):
        class EditPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.email = self.selenium.find_element_by_id('email')
                self.password = self.selenium.find_element_by_id('pass')
                self.fname = self.selenium.find_element_by_id('fname')
                self.lname = self.selenium.find_element_by_id('lname')
                self.phone = self.selenium.find_element_by_id('telephone')
                self.notif = self.selenium.find_element_by_xpath("//input[@type='radio' and @value='sms']")
                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return EditPage(self.selenium)

    @staticmethod
    def _fill(page):

        page.email.clear()
        page.password.clear()
        page.fname.clear()
        page.lname.clear()
        page.phone.clear()

        page.email.send_keys('parand1997@gmail.com')
        page.password.send_keys('123')
        page.fname.send_keys('Parand')
        page.lname.send_keys('Alizadeh')
        page.phone.send_keys('0234')
        page.notif.click()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_empty_parts_edit(self):
        page = self.__get_page()
        fields = [page.fname, page.lname, page.password, page.email, page.phone, page.notif]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)




    def test_successful_edit(self):
        page = self.__get_page()
        self._fill(page)

        page.button.click()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Edited Successfully")




