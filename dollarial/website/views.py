from django.shortcuts import render
import urllib.request
import json as simplejson


def contact(request):
    return render(request, 'website/contact.html')


def about(request):
    return render(request, 'website/about.html')


def history(request):
    return render(request, 'website/history.html')


def home(request):
    return render(request, 'website/home.html')


def currencies(request):
    response = urllib.request.urlopen("http://call.tgju.org/ajax.json")
    response_data = simplejson.load(response)
    euro = response_data['current']['price_eur']['p']
    euro = euro.replace(",", "")
    dollar = response_data['current']['price_dollar']['p']
    dollar = dollar.replace(",", "")
    rial_to_euro = 1 / float(euro)
    rial_to_dollar = 1 / float(dollar)
    euro_to_dollar = float(euro) / float(dollar)
    dollar_to_euro = float(dollar) / float(euro)
    currency_data = {
        "currencies": [
            {
                "name": "rial",
                "rial_value": "1",
                "dollar_value": rial_to_dollar,
                "euro_value": rial_to_euro,
            },
            {
                "name": "dollar",
                "rial_value": dollar,
                "dollar_value": "1",
                "euro_value": dollar_to_euro,
            },
            {
                "name": "euro",
                "rial_value": euro,
                "dollar_value": euro_to_dollar,
                "euro_value": "1",
            },
        ]
    }
    return render(request, 'website/currencies.html', currency_data)


def services(request):
    # TODO: read from db
    data = {
        "typeforms": [
            {
                "name": "Toefl",
                "type": "exam",
                "price": "200$",
                "details": "Toefl Exam",

            },
            {
                "name": "University Payment",
                "type": "University",
                "price": "unknown",
                "details": "University Fee",

            },
            {
                "name": "Transfer Money to Foreign Account",
                "type": "transfer",
                "price": "unknown",
                "details": "transfer to another countries",

            },
            {
                "name": "Transfer Money to Internal Account",
                "type": "transfer",
                "price": "unknown",
                "details": "transfer to Iran",

            },

        ]
    }
    return render(request, 'website/services.html', data)
