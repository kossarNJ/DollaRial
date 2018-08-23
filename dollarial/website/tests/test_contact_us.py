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
        self.assertIn("Department of Computer Enginerring,\n                                Sharif University of "
                      "Technology\n                        ", self.__get_text(address))
        self.assertIn("21 6600 5616", self.__get_text(phone))
        self.assertIn("dollarialsharif@gmail.com", self.__get_text(email))

    def __get_page(self):
        class ContactPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.name = self.selenium.find_element_by_id('id_name')
                self.email = self.selenium.find_element_by_id('id_email')
                self.subject = self.selenium.find_element_by_id('id_subject')
                self.message = self.selenium.find_element_by_id('id_message')
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
        contact_page.name.send_keys('Kossar Najafi')
        contact_page.email.send_keys('k_najafiaghdam@yahoo.com')
        self.__send_keys_scrolling(contact_page.subject, 'Thank You')
        self.__send_keys_scrolling(contact_page.message, 'Your website is the best! Thanks')
        contact_page.submit()
        _ = self.selenium.find_element_by_id('colorlib-hero')

    def test_posting_empty_message(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
        contact_page = self.__get_page()
        contact_page.name.send_keys('Kossar Najafi')
        contact_page.email.send_keys('k_najafiaghdam@yahoo.com')
        self.__send_keys_scrolling(contact_page.subject, 'Thank You')
        contact_page.submit()
        _ = self.selenium.find_element_by_id('colorlib-contact')
