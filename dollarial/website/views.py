from website.forms import ContactForm
from django.shortcuts import redirect
import sendgrid
from sendgrid.helpers.mail import *

from django.shortcuts import render
from dollarial.currency import get_dollar_rial_value
from dollarial.currency import get_euro_rial_value


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']

            sg = sendgrid.SendGridAPIClient(
                apikey='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')
            from_email = Email(email)
            to_email = Email("parand1997@gmail.com")
            subject = subject
            content = Content("text/plain", name + ":\n" + message)
            mail = Mail(from_email, subject, to_email, content)
            sg.client.mail.send.post(request_body=mail.get())

            return redirect('home')
    return render(request, "website/contact.html", {'form': form})


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
