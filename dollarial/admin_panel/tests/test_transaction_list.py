from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class TransactionListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.__create_transactions()

    @classmethod
    def tearDownClass(cls):
        # TODO: drop table
        pass

    @classmethod
    def __create_transactions(cls):
        # TODO: Add transactions and users
        pass

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/transactions'))

    def tearDown(self):
        # TODO: drop database
        self.selenium.quit()

    def test_not_logged_in_user_access(self):
        pass




self.client.login(username=superuser.username, password='superpassword') #Native django test client
cookie = self.client.cookies['sessionid']
self.browser.get(self.live_server_url + '/admin/')  #selenium will set cookie domain based on current page domain
self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
self.browser.refresh() #need to update page for logged in user
self.browser.get(self.live_server_url + '/admin/')