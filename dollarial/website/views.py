from django.shortcuts import render


def contact(request):
    return render(request, 'website/contact.html')


def about(request):
    return render(request, 'website/about.html')


def history(request):
    return render(request, 'website/history.html')


def home(request):
    return render(request, 'website/home.html')



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

