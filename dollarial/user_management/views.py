from django.shortcuts import render


def login(request):
    return render(request, 'user_management/login.html')


def registration(request):
    return render(request, 'user_management/registration.html')


def edit(request):
    data = {
        "user": {
            "fname": "kossar",
            "lname": "najafi",
            "email": "kossar.najafi@gmail.com",
            "phone": "09351234567",
        }
    }
    return render(request, 'user_management/edit_info.html', data)
