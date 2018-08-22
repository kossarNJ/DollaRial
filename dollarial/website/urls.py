from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('currencies/', views.currencies, name='currencies'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(pattern_name='home'))
]
