from django.shortcuts import render


def login(request):
    return render(request, 'user_management/login.html')


def registration(request):
    return render(request, 'user_management/signup.html')
