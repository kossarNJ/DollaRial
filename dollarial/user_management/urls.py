from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('edit/', views.edit, name='edit')
]