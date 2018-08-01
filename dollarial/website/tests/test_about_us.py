from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class AboutUsTestCase(StaticLiveServerTestCase):
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

    def test_about_text(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/about/'))
        about = self.selenium.find_element_by_id("about_text")
        people = self.selenium.find_element_by_id("people")
        self.assertIn("Something about us.", self.__get_text(about))
        self.assertIn("Our People \n\t\t\t\t\t\tSoroush Ebadian, Parand Alizade, Kosar Najafi", self.__get_text(people).strip())

    def test_about_contact_details(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/about/'))
        address = self.selenium.find_element_by_id("dollarial_address")
        phone = self.selenium.find_element_by_id("dollarial_phone")
        email = self.selenium.find_element_by_id("dollarial_email")
        self.assertIn("Department of Computer Enginerring, Sharif University of Technology", self.__get_text(address))
        self.assertIn("21 6600 5616", self.__get_text(phone))
        self.assertIn("dollarialsharif@gmail.com", self.__get_text(email))