from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings
from dollarial.models import User


class UserWalletsTest(StaticLiveServerTestCase):
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

    def setUp(self):
        self.user = User.objects.create_user(username="kossar",
                                             email="k_na@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    def login(self):
        user = User.objects.get(username="kossar")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(username="kossar").id
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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    def __add_data(self):
        wallets = [
            {"sign": "﷼",
             "credit": self.user.get_credit("R"),
             },
            {"sign": "$",
             "credit": self.user.get_credit("D"),
             },
            {"sign": "€",
             "credit": self.user.get_credit("E")
             }
        ]
        return wallets

    def test_view_wallets(self):
        self.login()
        data = self.__add_data()
        for d in data:
            credit = self.selenium.find_element_by_id("wallet_balance_" + d["sign"])
            self.assertEqual(float(d["credit"]), float(self.__get_text(credit)))
