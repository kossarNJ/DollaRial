from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic


from user_management.forms import SignUpForm


class Registration(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('user_index')
    template_name = 'user_management/registration.html'


class Login(SuccessMessageMixin, LoginView):
    template_name = 'user_management/login.html'
    redirect_field_name = reverse_lazy('user_index')
    success_message = "Hello %(username)s"


class Logout(LogoutView):
    next_page = reverse_lazy('home')
