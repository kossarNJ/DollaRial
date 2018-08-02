from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='user_transaction_list'),
    path('transactions/<int:transaction_id>', views.transaction_view, name='user_transaction_view'),
    path('profile/', views.edit_profile, name='user_edit_profile'),
    path('exchange/', views.exchange, name='user_exchange'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('payment_result/', views.payment_result, name='payment_result'),
    path('exchange/accept/', views.exchange_accept, name='user_exchange_accept'),
    path('', views.Index.as_view(), name='user_index'),
]
