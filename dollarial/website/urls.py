from django.urls import path

from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('home/', views.home, name='home'),
]
