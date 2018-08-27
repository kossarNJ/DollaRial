from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class CostumerListTest(StaticLiveServerTestCase):
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
        self.user = User.objects.create_user(username="kossar",
                                             email="k_naa@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.user = User.objects.create_user(username="soroush",
                                             email="soroush@gmail.com",
                                             password="likeicare",
                                             first_name="soroush",
                                             last_name="ebadian",
                                             phone_number="09147898557",
                                             account_number="1234567887654321",
                                             notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/'))

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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/costumers/'))

    def __get_costumers(self):
        class CostumerItem(object):
            def __init__(self, costumer_id, first_name, last_name, account_number, email, phone_number, active):
                self.costumer_id = costumer_id
                self.first_name = first_name
                self.last_name = last_name
                self.account_number = account_number
                self.email = email
                self.phone_number = phone_number
                self.active = active

        costumers = User.objects.all()
        result = []
        for costumer in costumers:
            result += [CostumerItem(costumer.id, costumer.first_name, costumer.last_name, costumer.account_number,
                                    costumer.email, costumer.phone_number, costumer.is_active)]
        return result

    def __get_page(self):
        class CostumerListPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.id = []
                self.first_name = []
                self.last_name = []
                self.account_number = []
                self.email = []
                self.phone_number = []
                self.active = []
                for i in range(1, 4):
                    self.id += [self.selenium.find_element_by_id('costumer_id_' + str(i))]
                    self.first_name += [self.selenium.find_element_by_id('costumer_fname_' + str(i))]
                    self.last_name += [self.selenium.find_element_by_id('costumer_lname_' + str(i))]
                    self.account_number += [self.selenium.find_element_by_id('costumer_account_number_' + str(i))]
                    self.email += [self.selenium.find_element_by_id('costumer_email_' + str(i))]
                    self.phone_number += [self.selenium.find_element_by_id('costumer_phone_number_' + str(i))]
                    self.active += [self.selenium.find_element_by_id('costumer_ban_status_' + str(i))]

        return CostumerListPage(self.selenium)

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        self.login()
        costumers = self.__get_costumers()
        page = self.__get_page()
        for i in range(3):
            self.assertIn(str(costumers[i].costumer_id), self.__get_text(page.id[i]))
            self.assertIn(costumers[i].first_name, self.__get_text(page.first_name[i]))
            self.assertIn(costumers[i].last_name, self.__get_text(page.last_name[i]))
            self.assertIn(str(costumers[i].account_number), self.__get_text(page.account_number[i]))
            self.assertIn(costumers[i].email, self.__get_text(page.email[i]))
            self.assertIn(str(costumers[i].phone_number), self.__get_text(page.phone_number[i]))
            self.assertIn(str(costumers[i].active), self.__get_text(page.active[i]))
