from dollarial.currency import Currency


class TransactionConstants(object):
    MIN_AMOUNT = {
        Currency.rial: 10000,
        Currency.dollar: 1,
        Currency.euro: 1
    }
    MAX_AMOUNT = {
        Currency.rial: 100000000,
        Currency.dollar: 10000,
        Currency.euro: 10000
    }

    MIN_EXCHANGE_FINAL_AMOUNT = 1
    MAX_EXCHANGE_FINAL_AMOUNT = 10000000

    MIN_CHARGE_DEPOSIT_AMOUNT = 1000
    MAX_CHARGE_AMOUNT = 100000000

    MIN_EXTERNAL_PAYMENT_AMOUNT = 10
    MAX_EXTERNAL_PAYMENT_AMOUNT = 10000

    MIN_INTERNAL_PAYMENT_AMOUNT = 1000
    MAX_INTERNAL_PAYMENT_AMOUNT = 100000000

    NORMAL_WAGE_PERCENTAGE = 9
    EXTERNAL_TRANSACTION_WAGE = 9

