from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='user_transaction_list'),
    path('transactions/<int:transaction_id>', views.transaction_view, name='user_transaction_view'),
    path('profile/', views.edit_profile, name='user_edit_profile'),
    path('', views.index, name='user_index'),
]
