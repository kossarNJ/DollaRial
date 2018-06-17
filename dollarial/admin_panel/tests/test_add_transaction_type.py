from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class TransactionTypeAddTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transaction_types/add'))
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
        class TransactionTypeAddPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.name = self.selenium.find_element_by_id('cc-name')
                self.description = self.selenium.find_element_by_id('cc-description')
                self.fixed_price = self.selenium.find_element_by_id('cc-fixed-price')
                self.currency_select = self.selenium.find_element_by_id('currency-select')
                self.price = self.selenium.find_element_by_id('cc-price')
                self.min_price = self.selenium.find_element_by_id('cc-min-price')
                self.max_price = self.selenium.find_element_by_id('cc-max-price')
                self.wage = self.selenium.find_element_by_id('cc-wage')
                self.personal_info = self.selenium.find_element_by_id('personal-info')
                self.public_info = self.selenium.find_element_by_id('public-info')
                self.university_info = self.selenium.find_element_by_id('university-info')
                self.Quiz_info = self.selenium.find_element_by_id('Quiz-info')

                self.save_button = self.selenium.find_element_by_id('save_button')
                self.reset_button = self.selenium.find_element_by_id('reset_button')

        return TransactionTypeAddPage(self.selenium)

    def check_transaction_type_creation(self):
        # TODO: check transaction type GRE creation
        pass

    @staticmethod
    def _fill(page):
        page.name.send_keys('GRE')
        page.description.send_keys('english exam')
        page.fixed_price.click()

        for option in page.currency_select.find_elements_by_tag_name('option'):
            if option.text == 'Dollar':
                option.click()
                break
        page.price.send_keys('300')
        page.min_price.send_keys('10')
        page.max_price.send_keys('1000')
        page.wage.send_keys('5')
        page.personal_info.click()
        page.public_info.click()

    @staticmethod
    def _login(page):  # TODO
        pass

    def test_not_loggedin(self):  # TODO
        pass

    def test_successful_ttadd(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.save_button.click()
        self.check_transaction_type_creation()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Transaction Type Added Successfully")

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    def test_empty_parts_add(self):
        page = self.__get_page()
        self._login(page)
        fields = [page.name, page.description, page.fixed_price, page.currency_select, page.price, page.min_price,
                  page.max_price, page.wage, page.personal_info, page.public_info, page.university_info, page.Quiz_info]
        self._fill(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.save_button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)

    def test_already_existing_transaction_type(self):
        page = self.__get_page()
        self._login(page)
        self._fill(page)
        page.name.clear()
        page.name.send_keys('Toefl')
        page.save_button.click()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "There exists a Transaction Type with entered name.")

    def test_reset_button(self):
        page = self.__get_page()
        self._login(page)
        text_fields = [page.name, page.description, page.price, page.min_price, page.max_price, page.wage]
        self._fill(page)
        page.reset_button.click()
        for field in text_fields:
            self.assertEqual(self.__get_text(field), "")
        checkboxes = [page.fixed_price, page.personal_info, page.public_info, page.university_info, page.Quiz_info]
        for checkbox in checkboxes:
            self.assertEqual(self.__get_checked(checkbox), 'false')
