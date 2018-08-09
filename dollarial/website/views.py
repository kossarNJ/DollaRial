from website.forms import ContactForm
from django.shortcuts import render, redirect
import sendgrid
from sendgrid.helpers.mail import *


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

            sg = sendgrid.SendGridAPIClient(apikey='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')
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
    data = {
        "c":{
        "name1": "dollar",
        "name2": "rial",
        "amount": "1",
        "result": "42000",
        }
    }
    return render(request, 'website/currencies.html', data)


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

