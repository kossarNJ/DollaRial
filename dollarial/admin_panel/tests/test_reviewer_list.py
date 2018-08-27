from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User, Clerk
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class ReviewerListTest(StaticLiveServerTestCase):
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
        self.user = User.objects.create_superuser(username="kossar_admin",
                                                  email="k_na@gmail.com",
                                                  password="likeicare",
                                                  first_name="kossar",
                                                  last_name="najafi",
                                                  phone_number="09147898557",
                                                  account_number="1234567812345678",
                                                  notification_preference="S")
        self.user1 = User.objects.create_user(username="kossar",
                                              email="k_naa@gmail.com",
                                              password="likeicare",
                                              first_name="kossar",
                                              last_name="najafi",
                                              phone_number="09147898557",
                                              account_number="1234432112344321",
                                              is_staff=True,
                                              notification_preference="S")
        self.user2 = User.objects.create_user(username="soroush",
                                              email="soroush@gmail.com",
                                              password="likeicare",
                                              first_name="soroush",
                                              last_name="ebadian",
                                              phone_number="09147898557",
                                              account_number="1234567887654321",
                                              notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/'))

    def login(self):
        user = User.objects.get(username="kossar_admin")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(username="kossar_admin").id
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        }

        self.selenium.add_cookie(cookie)
        self.selenium.refresh()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/1'))

    def create_reviewer(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))
        username = Select(self.selenium.find_element_by_id('id_user'))
        salary = self.selenium.find_element_by_id('id_salary')
        button = self.selenium.find_element_by_xpath("//button[@type='submit']")
        username.select_by_visible_text('kossar')
        salary.clear()
        salary.send_keys("2000")
        button.click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/add'))
        username = Select(self.selenium.find_element_by_id('id_user'))
        salary = self.selenium.find_element_by_id('id_salary')
        button = self.selenium.find_element_by_xpath("//button[@type='submit']")
        username.select_by_visible_text('soroush')
        salary.clear()
        salary.send_keys("1000")
        button.click()

    def __get_reviewers(self):
        class ReviewerItem(object):
            def __init__(self, reviewer_id, username, salary, is_employee):
                self.reviewer_id = reviewer_id
                self.username = username
                self.salary = salary
                self.is_employee = is_employee

        reviewers = Clerk.objects.all()
        result = []
        for reviewer in reviewers:
            result += [ReviewerItem(reviewer.id, reviewer.user.username, reviewer.salary, reviewer.is_employee)]
        return result

    def __get_page(self):
        class ReviewerListPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = []
                self.username = []
                self.salary = []
                self.is_employee = []
                for i in range(1, 3):
                    self.id += [self.selenium.find_element_by_id('reviewer_id_' + str(i))]
                    self.username += [self.selenium.find_element_by_id('reviewer_username_' + str(i))]
                    self.salary += [self.selenium.find_element_by_id('reviewer_salary_' + str(i))]
                    self.is_employee += [self.selenium.find_element_by_id('reviewer_is_employee_' + str(i))]

        return ReviewerListPage(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        self.login()
        self.create_reviewer()
        reviewers = self.__get_reviewers()
        page = self.__get_page()
        for i in range(2):
            self.assertIn(str(reviewers[i].reviewer_id), self.__get_text(page.id[i]))
            self.assertIn(reviewers[i].username, self.__get_text(page.username[i]))
            self.assertIn(str(reviewers[i].salary), self.__get_text(page.salary[i]))
            self.assertIn(str(reviewers[i].is_employee), self.__get_text(page.is_employee[i]))
