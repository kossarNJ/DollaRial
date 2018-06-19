from django.test import TestCase


class AfterReviewCreditBalanceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: setup Database
        pass

    @staticmethod
    def __get_currency(currency_type):
        # TODO: get currency in Rials
        return 0

    @staticmethod
    def __set_currency(currency_type, value):
        # TODO: get currency in Rials
        pass

    @staticmethod
    def __update_currencies():
        # TODO: call update function
        pass

    def test_update(self):
        self.__set_currency("dollar", 0)
        self.__set_currency("euro", 0)
        self.__update_currencies()
        self.assertGreater(self.__get_currency("dollar"), 0)
        self.assertGreater(self.__get_currency("euro"), 0)
