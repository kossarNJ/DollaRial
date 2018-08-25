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
        soroush = self.selenium.find_element_by_id("soroush")
        parand = self.selenium.find_element_by_id("parand")
        kossar = self.selenium.find_element_by_id("kossar")
        self.assertIn("\n                            Our team brings together some of the brightest Computer "
                      "Engineering students of Sharif University of Technology.\n                            The team "
                      "is a perfect system seeing as it is a combination of people whose skills fit together like "
                      "pieces of a puzzle.\n                            Their youth and creativity brings innovation "
                      "to their work.\n                        ", self.__get_text(about))
        self.assertIn("Soroush Ebadian", self.__get_text(soroush))
        self.assertIn("Parand Alizade", self.__get_text(parand))
        self.assertIn("Kossar Najafi", self.__get_text(kossar))

    def test_about_contact_details(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/about/'))
        address = self.selenium.find_element_by_id("dollarial_address")
        phone = self.selenium.find_element_by_id("dollarial_phone")
        email = self.selenium.find_element_by_id("dollarial_email")
        self.assertIn("Department of Computer Enginerring,", self.__get_text(address))
        self.assertIn("21 6600 5616", self.__get_text(phone))
        self.assertIn("dollarialsharif@gmail.com", self.__get_text(email))