from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class ServicesTestCase(StaticLiveServerTestCase):
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


    def __add_data(self):

        #todo add to db
        data = [
                {
                    "name": "Toefl",
                    "type": "exam",
                    "price": "200$",
                    "details": "Toefl Exam",

                },
                {
                    "name": "University Payment",
                    "type": "University",
                    "price": "unknown",
                    "details": "University Fee",

                },
                {
                    "name": "Transfer Money to Foreign Account",
                    "type": "transfer",
                    "price": "unknown",
                    "details": "transfer to another countries",

                },
                {
                    "name": "Transfer Money to Internal Account",
                    "type": "transfer",
                    "price": "unknown",
                    "details": "transfer to Iran",

                },

            ]
        return data


    def test_services(self):
        data = self.__add_data()
        self.selenium.get('%s%s' % (self.live_server_url, '/services/'))
        i = 0
        for d in data:
            name = self.selenium.find_element_by_id("name_" + str(i))
            t = self.selenium.find_element_by_id("type_" + str(i))
            price = self.selenium.find_element_by_id("price_"+ str(i))
            details = self.selenium.find_element_by_id("details_" + str(i))
            self.assertIn(d["name"], self.__get_text(name))
            self.assertIn(d["type"], self.__get_text(t))
            self.assertIn(d["price"], self.__get_text(price))
            self.assertIn(d["details"], self.__get_text(details))
            i = i + 1



#TODO click on each service?