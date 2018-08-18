from enum import Enum
import urllib.request
import json as simplejson


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


def get_euro_rial_value():
    response = urllib.request.urlopen("http://call.tgju.org/ajax.json")
    response_data = simplejson.load(response)
    euro = response_data['current']['price_eur']['p']
    euro = euro.replace(",", "")
    return float(euro)


def get_dollar_rial_value():
    response = urllib.request.urlopen("http://call.tgju.org/ajax.json")
    response_data = simplejson.load(response)
    dollar = response_data['current']['price_dollar']['p']
    dollar = dollar.replace(",", "")
    return float(dollar)
