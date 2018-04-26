from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from seleniumtest.models import Question


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

        q0 = Question.objects.create(question_text='halet chetore?')
        q1 = Question.objects.create(question_text='hava khube?')
        q0.save()
        q1.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_index(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/seleniumtest/'))
        print("address:", self.live_server_url)
        question0 = self.selenium.find_element_by_name("question_1")
        question1 = self.selenium.find_element_by_name("question_2")
        self.selenium.find_element_by_xpath('//li[@name="question_1"]/a').click()
