from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='admin_transaction_list'),
    path('transactions/<int:transaction_id>', views.transaction_view, name='admin_transaction_view'),
    path('reviewers/', views.reviewer_list, name='admin_reviewer_list'),
    path('reviewers/<int:reviewer_id>', views.reviewer_view, name='admin_reviewer_view'),
    path('reviewer/add/', views.reviewer_add, name='admin_reviewer_add'),
    path('customers/', views.costumer_list, name='admin_costumer_list'),
    path('costumers/<int:costumer_id>', views.costumer_view, name='admin_costumer_view'),
    path('skipped/', views.skipped_transaction_list, name='admin_skipped_transaction_list'),
    path('', views.index, name='admin_index'),
]
