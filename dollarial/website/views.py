from django.shortcuts import render


def contact(request):
    return render(request, 'website/contact.html')


def about(request):
    return render(request, 'website/about.html')


def history(request):
    return render(request, 'website/history.html')


def home(request):
    return render(request, 'website/home.html')
