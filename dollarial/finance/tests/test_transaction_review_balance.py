from django.test import TestCase


class AfterReviewCreditBalanceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: create users and transaction types
        # user1 credit=100
        # user2 credit=100
        cls.system_id = 100
        pass

    @staticmethod
    def __create_transaction():
        # TODO: create transaction
        return None

    @staticmethod
    def __reject_transaction(transaction):
        # TODO: run reject function
        pass

    @staticmethod
    def __accept_transaction(transaction):
        # TODO: run accept function
        pass

    @staticmethod
    def __skip_transaction(transaction):
        # TODO: run skip function
        pass

    @staticmethod
    def __get_credit(user_id):
        # TODO: get user credit
        return 0

    def test_rejection(self):
        transaction = self.__create_transaction()
        self.assertEqual(self.__get_credit(1), 0)
        self.assertEqual(self.__get_credit(self.system_id), 100)
        self.assertEqual(self.__get_credit(2), 100)
        self.__reject_transaction(transaction)
        self.assertEqual(self.__get_credit(1), 100)
        self.assertEqual(self.__get_credit(self.system_id), 0)
        self.assertEqual(self.__get_credit(2), 100)

    def test_acceptance(self):
        transaction = self.__create_transaction()
        self.assertEqual(self.__get_credit(1), 0)
        self.assertEqual(self.__get_credit(self.system_id), 100)
        self.assertEqual(self.__get_credit(2), 100)
        self.__accept_transaction(transaction)
        self.assertEqual(self.__get_credit(1), 0)
        self.assertEqual(self.__get_credit(self.system_id), 7)
        self.assertEqual(self.__get_credit(2), 193)

    def test_skip(self):
        transaction = self.__create_transaction()
        self.assertEqual(self.__get_credit(1), 0)
        self.assertEqual(self.__get_credit(self.system_id), 100)
        self.assertEqual(self.__get_credit(2), 100)
        self.__skip_transaction(transaction)
        self.assertEqual(self.__get_credit(1), 0)
        self.assertEqual(self.__get_credit(self.system_id), 100)
        self.assertEqual(self.__get_credit(2), 100)
