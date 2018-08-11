from dollarial.currency import Currency


class TransactionConstants(object):
    MIN_AMOUNT = {
        Currency.rial: 1,
        Currency.dollar: 1,
        Currency.euro: 1
    }
    MAX_AMOUNT = {
        Currency.rial: 1000000,
        Currency.dollar: 10000,
        Currency.euro: 10000
    }
    NORMAL_WAGE_PERCENTAGE = 9
