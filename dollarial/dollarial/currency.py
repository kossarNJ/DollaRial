from enum import Enum


class Currency(Enum):
    dollar = ('D', "Dollar", "Dollars", '$')
    rial = ('R', "Rial", "Rials", '﷼')
    euro = ('E', "Euro", "Euros", '€')

    def __init__(self, char, name, plural, sign):
        self.char = char
        self.display_name = name
        self.display_name_plural = plural
        self.sign = sign

    @classmethod
    def choices(cls):
        return tuple((i.char, i.display_name) for i in cls)

    @classmethod
    def get_all_currencies(cls):
        return [x for x in cls]

    @classmethod
    def get_all_currency_chars(cls):
        return [currency.char for currency in cls]
