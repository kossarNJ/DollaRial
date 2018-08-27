from website.forms import ContactForm
from django.shortcuts import redirect
from django.shortcuts import render
from dollarial.currency import get_dollar_rial_value
from dollarial.currency import get_euro_rial_value
from dollarial.models import send_email_to_user
from dollarial.settings import ADMIN_EMAIL

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            to_email = ADMIN_EMAIL
            content = name + ":\n" + message
            send_email_to_user(subject, from_email, to_email, content)

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
