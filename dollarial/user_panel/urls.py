from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='user_transaction_list'),
    path('transactions/<int:transaction_id>', views.transaction_view, name='user_transaction_view'),
    path('profile/', views.ProfileUpdate.as_view(), name='user_edit_profile'),
    path('exchange/', views.Exchange.as_view(), name='user_exchange'),
    path('charge/', views.ChargeCredit.as_view(), name='user_charge'),
    path('deposit/', views.DepositCredit.as_view(), name='user_deposit'),
    path('payment_form/<int:payment_type_id>', views.ServicePayment.as_view(), name='payment_form'),
    path('payment_form/<int:payment_type_id>/confirmation/', views.ServicePaymentConfirmation.as_view(),
         name='payment_form_confirmation'),
    path('internal_payment/', views.InternalPayment.as_view(), name='internal_payment'),
    path('external_payment/', views.ExternalPayment.as_view(), name='external_payment'),
    path('external_payment/confirmation/', views.ExternalPaymentConfirmation.as_view(),
         name='external_payment_confirmation'),
    path('exchange/accept/', views.ExchangeConfirmation.as_view(), name='user_exchange_accept'),
    path('services/', views.Services.as_view(), name='user_services'),
    path('', views.Index.as_view(), name='user_index'),
]
