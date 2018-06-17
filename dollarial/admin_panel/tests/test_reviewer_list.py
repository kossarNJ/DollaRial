from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ReviewerListTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.__create_reviewers()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin_panel/reviewers/'))

    @classmethod
    def __create_reviewers(self):
        # TODO: insert reviewers to DB with fields of ReviewerItem
        pass

    def __get_reviewers(self):
        # TODO: get list of reviewers from DB
        class ReviewerItem(object):
            def __init__(self, reviewer_id, reviewer_username, reviewer_salary):
                self.reviewer_id = reviewer_id
                self.reviewer_username = reviewer_username
                self.reviewer_salary = reviewer_salary

        return [ReviewerItem("1", "soroush", "200000"),
                ReviewerItem("2", "parand", "210000"), ReviewerItem("3", "kosar", "10000")]

    def __get_page(self):
        class ReviewerListPage(object):
            def __init__(self, selenium, my_list):
                self.selenium = selenium
                self.id = []
                self.reviewer_username = []
                self.reviewer_salary = []

                for row in my_list:
                    self.id += [self.selenium.find_element_by_id('reviewer_id_' + row.reviewer_id)]
                    self.reviewer_username += [self.selenium.find_element_by_id('reviewer_username_' + row.reviewer_id)]
                    self.reviewer_salary += [self.selenium.find_element_by_id('reviewer_salary_' + row.reviewer_id)]

        return ReviewerListPage(self.selenium, self.__get_reviewers())

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_fields_content(self):
        reviewers = self.__get_reviewers()
        page = self.__get_page()
        i = 0
        for item in reviewers:
            self.assertEqual(item.reviewer_id, self.__get_text(page.id[i]))
            self.assertEqual(item.reviewer_username, self.__get_text(page.reviewer_username[i]))
            self.assertEqual(item.reviewer_salary, self.__get_text(page.reviewer_salary[i]))
            i += 1

    def test_not_logged_in_user_access(self):
        # TODO: implement. Non_manager user should not be able to access this page.
        pass

    def test_logged_in_user_access(self):
        # TODO: implement. Manager user should be able to access this page.
        pass
