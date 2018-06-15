from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='admin_transaction_list'),
    path('reviewers/', views.reviewer_list, name='admin_reviewer_list'),
    path('customers/', views.costumer_list, name='admin_costumer_list'),
    path('skipped/', views.skipped_transaction_list, name='admin_skipped_transaction_list'),
    path('', views.index, name='admin_index'),
]