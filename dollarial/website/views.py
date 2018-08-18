from django.shortcuts import render
from dollarial.currency import get_dollar_rial_value
from dollarial.currency import get_euro_rial_value


def contact(request):
    return render(request, 'website/contact.html')


def about(request):
    return render(request, 'website/about.html')


def history(request):
    return render(request, 'website/history.html')


def home(request):
    return render(request, 'website/home.html')


def currencies(request):
    euro = get_euro_rial_value()
    dollar = get_dollar_rial_value()
    rial_to_euro = 1 / euro
    rial_to_dollar = 1 / dollar
    euro_to_dollar = euro / dollar
    dollar_to_euro = dollar / euro
    currency_data = {
        "currencies": [
            {
                "name": "rial",
                "rial_value": "1",
                "dollar_value": str(rial_to_dollar),
                "euro_value": str(rial_to_euro),
            },
            {
                "name": "dollar",
                "rial_value": str(dollar),
                "dollar_value": "1",
                "euro_value": str(dollar_to_euro),
            },
            {
                "name": "euro",
                "rial_value": str(euro),
                "dollar_value": str(euro_to_dollar),
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
