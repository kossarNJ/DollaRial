from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from user_management.forms import SignUpForm


class Registration(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('user_index')
    template_name = 'user_management/registration.html'


class Login(LoginView):
    template_name = 'user_management/login.html'
    redirect_field_name = reverse_lazy('user_index')
