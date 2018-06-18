from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ViewWalletTest(StaticLiveServerTestCase):
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
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/'))

    @classmethod
    def __create_wallets(self):
        # TODO: insert wallets to DB with fields of WalletItem
        pass

    def __get_wallets(self):
        # TODO: get list of wallets from DB
        class WalletItem(object):
            def __init__(self, wallet_name, wallet_balance):
                self.wallet_name = wallet_name
                self.wallet_balance = wallet_balance

        return [WalletItem("dollar", "2200"), WalletItem("rial", "1000"), WalletItem("euro", "1020")]

    def __get_page(self):
        class IndexPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.balance = []
                for wallet in my_list:
                    self.balance += [self.selenium.find_element_by_id('wallet_balance_' + wallet.wallet_name)]

        return IndexPage(self.selenium, self.__get_wallets())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    @staticmethod
    def _login(page):  # TODO
        pass

    def test_not_loggedIn(self):  # TODO
        pass

    def test_not_user(self):  # TODO
        pass

    def test_fields_content(self):
        page = self.__get_page()
        self._login(page)
        wallets = self.__get_wallets()
        i = 0
        for item in wallets:
            self.assertEqual(item.wallet_balance, self.__get_text(page.balance[i]))
            i += 1





