from importlib import import_module
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class ExchangeCreditTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        self.user = User.objects.create_user(username="kossar",
                                             email="k_na@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/exchange/'))

    def tearDown(self):
        self.selenium.quit()

    def __get_page_1(self):
        class ExchangePage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.from_curr = Select(self.selenium.find_element_by_id('id_currency'))
                self.to_curr = Select(self.selenium.find_element_by_id('id_final_currency'))
                self.amount = self.selenium.find_element_by_id('id_final_amount')
                self.button = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return ExchangePage(self.selenium)

    def __get_page_2(self):
        class ExchangePreviewPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.confirm_exchange = self.selenium.find_element_by_xpath("//button[@type='submit']")

        return ExchangePreviewPage(self.selenium)

    @staticmethod
    def _fill_1(page):
        page.amount.send_keys('1')
        page.from_curr.select_by_visible_text('﷼')
        page.to_curr.select_by_visible_text('$')

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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/exchange/'))

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def charge_wallet(self, amount):
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/charge/'))
        self.selenium.find_element_by_id('id_amount').send_keys(amount)
        self.selenium.find_element_by_id('charge-button').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/exchange/'))

    def test_preview_exchange_not_empty(self):
        self.login()
        page = self.__get_page_1()
        self._fill_1(page)

        page.amount.clear()
        page.button.click()
        success_set = self.selenium.find_elements_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertEqual(len(success_set), 0)
        page.amount.send_keys('1')

        page.from_curr.select_by_visible_text('---------')
        page.button.click()
        success_set = self.selenium.find_elements_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertEqual(len(success_set), 0)
        page.from_curr.select_by_visible_text('﷼')

        page.to_curr.select_by_visible_text('---------')
        page.button.click()
        success_set = self.selenium.find_elements_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertEqual(len(success_set), 0)
        page.to_curr.select_by_visible_text('$')

    def test_preview_exchange(self):
        self.login()
        self.charge_wallet(550000)
        page = self.__get_page_1()
        self._fill_1(page)
        page.button.click()
        self.selenium.implicitly_wait(10)
        self.assertIn("accept", self.selenium.current_url)

    def test_preview_accept(self):
        self.login()
        self.charge_wallet(550000)
        page = self.__get_page_1()
        self._fill_1(page)
        page.button.click()
        self.selenium.implicitly_wait(10)

        page2 = self.__get_page_2()
        page2.confirm_exchange.click()
        time.sleep(3)
        credit = self.selenium.find_element_by_id("wallet_balance_$")
        self.assertEqual(float(1), float(self.__get_text(credit)))
        self.assertNotIn("accept", self.selenium.current_url)
