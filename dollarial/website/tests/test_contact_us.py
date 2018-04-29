from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class ContactUsTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_contact_details(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
        address = self.selenium.find_element_by_id("dollarial_address")
        phone = self.selenium.find_element_by_id("dollarial_phone")
        email = self.selenium.find_element_by_id("dollarial_email")
        self.assertIn("Department of Computer Enginerring, Sharif University of Technology", self.__get_text(address))
        self.assertIn("21 6600 5616", self.__get_text(phone))
        self.assertIn("dollarialsharif@gmail.com", self.__get_text(email))

    def __get_page(self):
        class ContactPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.fname = self.selenium.find_element_by_id('fname')
                self.lname = self.selenium.find_element_by_id('lname')
                self.email = self.selenium.find_element_by_id('email')
                self.subject = self.selenium.find_element_by_xpath('//input[@id="subject"]')
                self.message = self.selenium.find_element_by_id('message')
                self.button = self.selenium.find_element_by_xpath("//input[@class='btn btn-primary']")

            def submit(self):
                self.button.click()

        return ContactPage(self.selenium)

    @staticmethod
    def __send_keys_scrolling(input_element, keys):
        _ = input_element.location_once_scrolled_into_view
        time.sleep(1)
        input_element.send_keys(keys)

    def test_posting_message(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
        contact_page = self.__get_page()
        contact_page.fname.send_keys('Soroush')
        contact_page.lname.send_keys('Ebadian')
        contact_page.email.send_keys('soroush@divar.ir')
        self.__send_keys_scrolling(contact_page.subject, 'Thank You')
        self.__send_keys_scrolling(contact_page.message, 'Your website is the best! Thanks')
        contact_page.submit()
        success = self.selenium.find_element_by_css_selector('.success')
        self.assertEqual(success.text, "Thank you! Your message is sent to DollaRial.")

    def test_posting_empty_message(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
        contact_page = self.__get_page()
        contact_page.fname.send_keys('Soroush')
        contact_page.lname.send_keys('Ebadian')
        contact_page.email.send_keys('soroush@divar.ir')
        self.__send_keys_scrolling(contact_page.subject, 'Thank You')
        contact_page.submit()
        error = self.selenium.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Please enter your message.")
