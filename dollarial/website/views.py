from django.shortcuts import render


def contact(request):
    return render(request, 'website/contact.html')
