from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time


class PaymentFormTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/payment_form'))

    def __login(self):
        pass

    def __get_form_page(self):
        class FormPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.fname = self.selenium.find_element_by_id('fname')
                self.lname = self.selenium.find_element_by_id('lname')
                self.phone = self.selenium.find_element_by_id('telephone')

                self.security = self.selenium.find_element_by_id('security_number')
                self.passport = self.selenium.find_element_by_id('passport_number')

                self.exam_user = self.selenium.find_element_by_id('exam_user')
                self.exam_pass = self.selenium.find_element_by_id('exam_pass')
                self.exam_date = self.selenium.find_element_by_id('exam_date')
                self.exam_country = self.selenium.find_element_by_id('exam_country')
                self.exam_center = self.selenium.find_element_by_id('exam_center')

                self.uni_link = self.selenium.find_element_by_id('uni_link')
                self.uni_user = self.selenium.find_element_by_id('uni_user')
                self.uni_pass = self.selenium.find_element_by_id('uni_pass')

                self.amount = self.selenium.find_element_by_id('amount')
                self.unit = self.selenium.find_element_by_xpath("//input[@type='radio' and @value='dollar']")
                self.account = self.selenium.find_element_by_id('account')


                self.amount_sec = self.selenium.find_element_by_id('amount')
                self.account_sec = self.selenium.find_element_by_id('account')

                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return FormPage(self.selenium)


    def __get_result_page(self):
        class ResultPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.rtype = self.selenium.find_element_by_id('cc-type')
                self.ramount = self.selenium.find_element_by_id('cc-type')
                self.rdestination = self.selenium.find_element_by_id('cc-type')
                self.rcontinue = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

        return ResultPage(self.selenium)

    @staticmethod
    def __get_value(element):
        return element.get_attribute('value')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def __get_checked(element):
        return element.get_attribute('checked')

    @staticmethod
    def _fill_university(page):

        _ = page.fname.location_once_scrolled_into_view
        time.sleep(0.1)
        page.fname.send_keys('parand')

        _ = page.lname.location_once_scrolled_into_view
        time.sleep(0.1)
        page.lname.send_keys('alizadeh')

        _ = page.phone.location_once_scrolled_into_view
        time.sleep(0.1)
        page.phone.send_keys('1234')

        _ = page.uni_link.location_once_scrolled_into_view
        time.sleep(0.1)
        page.uni_link.send_keys('mse.stanford.org')

        _ = page.uni_user.location_once_scrolled_into_view
        time.sleep(0.1)
        page.uni_user.send_keys('parand')

        _ = page.uni_pass.location_once_scrolled_into_view
        time.sleep(0.1)
        page.uni_pass.send_keys('1234')


    @staticmethod
    def _fill_exam(page):
        _ = page.fname.location_once_scrolled_into_view
        time.sleep(0.1)
        page.fname.send_keys('parand')

        _ = page.lname.location_once_scrolled_into_view
        time.sleep(0.1)
        page.lname.send_keys('alizadeh')

        _ = page.phone.location_once_scrolled_into_view
        time.sleep(0.1)
        page.phone.send_keys('1234')

        _ = page.passport.location_once_scrolled_into_view
        time.sleep(0.1)
        page.passport.send_keys('123456')

        _ = page.security.location_once_scrolled_into_view
        time.sleep(0.1)
        page.security.send_keys('1234')

        _ = page.exam_pass.location_once_scrolled_into_view
        time.sleep(0.1)
        page.exam_pass.send_keys('1234')

        _ = page.exam_user.location_once_scrolled_into_view
        time.sleep(0.1)
        page.exam_user.send_keys('parand')

        _ = page.exam_center.location_once_scrolled_into_view
        time.sleep(0.1)
        page.exam_center.send_keys('LA')

        _ = page.exam_country.location_once_scrolled_into_view
        time.sleep(0.1)
        page.exam_country.send_keys('US')

        _ = page.exam_date.location_once_scrolled_into_view
        time.sleep(0.1)
        page.exam_date.send_keys('01/07')


    @staticmethod
    def _fill_transfer(page):

        _ = page.amount.location_once_scrolled_into_view
        time.sleep(0.1)
        page.amount.send_keys('10000')

        _ = page.account.location_once_scrolled_into_view
        time.sleep(0.1)
        page.account.send_keys('1234')

        _ = page.unit.location_once_scrolled_into_view
        time.sleep(0.1)
        page.unit.click()

    @staticmethod
    def _fill_internal(page):
        _ = page.amount_sec.location_once_scrolled_into_view
        time.sleep(0.1)
        page.amount_sec.send_keys('10000')

        _ = page.account_sec.location_once_scrolled_into_view
        time.sleep(0.1)
        page.account_sec.send_keys('1234')




    def test_empty_parts_university(self):

        #todo if university
        self.__login()
        page = self.__get_form_page()
        fields = [page.fname, page.lname, page.phone, page.uni_link, page.uni_user, page.uni_pass]
        self._fill_university(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)


    def test_empty_parts_exam(self):

        #todo if exam
        self.__login()
        page = self.__get_form_page()
        fields = [page.fname, page.lname, page.phone, page.passport, page.security, page.exam_center, page.exam_country, page.exam_date, page.exam_pass, page.exam_user]
        self._fill_exam(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)



    def test_empty_parts_transfer(self):

        #todo if transfer
        self.__login()
        page = self.__get_form_page()
        fields = [page.amount, page.account, page.unit]
        self._fill_transfer(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)



    def test_empty_parts_internal(self):

        #todo if internal
        self.__login()
        page = self.__get_form_page()
        fields = [page.amount_sec, page.account_sec]
        self._fill_internal(page)
        for field in fields:
            prev_text = self.__get_text(field)
            field.clear()
            page.button.click()
            error = self.selenium.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "Please fill all required fields.")
            field.send_keys(prev_text)





    def __add_data(self):
        #TODO add db
        data = {
            "type": "University",
            "amount": "200 $",
            "destination": "Stanford University",
        }
        return data
    def test_success_university(self):


        #todo if university
        data = self.__add_data()
        self.__login()
        page = self.__get_form_page()
        self._fill_university(page)

        page.button.click()
        time.sleep(1)

        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/payment_result'))
        p = self.__get_result_page()
        self.assertEqual(data["amount"], self.__get_text(p.ramount))
        self.assertEqual(data["type"], self.__get_text(p.rtype))
        self.assertEqual(data["destination"], self.__get_text(p.rdestination))

        p.rcontinue.click()

        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Payment is completed")




    def test_success_exam(self):

        #todo if exam
        data = self.__add_data()
        self.__login()
        page = self.__get_form_page()
        self._fill_exam(page)

        page.button.click()
        time.sleep(1)

        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/payment_result'))
        p = self.__get_result_page()
        self.assertEqual(data["amount"], self.__get_text(p.ramount))
        self.assertEqual(data["type"], self.__get_text(p.rtype))
        self.assertEqual(data["destination"], self.__get_text(p.rdestination))

        p.rcontinue.click()

        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Payment is completed")



    def test_success_transfer(self):

        #todo if transfer
        data = self.__add_data()
        self.__login()
        page = self.__get_form_page()
        self._fill_transfer(page)

        page.button.click()
        time.sleep(1)

        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/payment_result'))
        p = self.__get_result_page()
        self.assertEqual(data["amount"], self.__get_text(p.ramount))
        self.assertEqual(data["type"], self.__get_text(p.rtype))
        self.assertEqual(data["destination"], self.__get_text(p.rdestination))

        p.rcontinue.click()

        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Payment is completed")




    def test_success_internal(self):

        #todo if internal
        data = self.__add_data()
        self.__login()
        page = self.__get_form_page()
        self._fill_internal(page)

        page.button.click()
        time.sleep(1)

        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/payment_result'))
        p = self.__get_result_page()
        self.assertEqual(data["amount"], self.__get_text(p.ramount))
        self.assertEqual(data["type"], self.__get_text(p.rtype))
        self.assertEqual(data["destination"], self.__get_text(p.rdestination))

        p.rcontinue.click()

        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Payment is completed")



    def test_logged_in_user_access(self):
        # TODO: implement.  user should be able to access this page.
        pass
