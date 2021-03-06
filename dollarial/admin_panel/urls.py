from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.TransactionList.as_view(), name='admin_transaction_list'),
    path('transactions/<int:transaction_id>', views.TransactionView.as_view(), name='admin_transaction_view'),
    path('reviewers/', views.ClerkList.as_view(), name='admin_reviewer_list'),
    path('reviewers/<int:pk>', views.ClerkUpdate.as_view(), name='admin_reviewer_view'),
    path('reviewers/add/', views.ClerkAdd.as_view(), name='admin_reviewer_add'),
    path('costumers/', views.UserList.as_view(), name='admin_costumer_list'),
    path('costumers/<int:pk>', views.UserUpdate.as_view(), name='admin_costumer_view'),
    path('skipped/', views.SkippedTransactionsHistory.as_view(), name='admin_skipped_transaction_list'),
    path('reviewed/', views.ReviewedTransactionsHistory.as_view(), name='admin_reviewed_transaction_history'),
    path('transaction_types/', views.PaymentTypeList.as_view(), name='admin_transaction_type_list'),
    path('transaction_types/add/', views.PaymentTypeAdd.as_view(), name='admin_transaction_type_add'),
    path('transaction_types/<int:pk>', views.PaymentTypeView.as_view(),
         name='admin_transaction_type_view'),
    path('reports/', views.ReportList.as_view(), name='admin_report_list'),
    path('transaction_group/', views.TransactionGroupList.as_view(), name='admin_transaction_group_list'),
    path('transaction_group/<int:pk>', views.TransactionGroupView.as_view(), name='admin_transaction_group_view'),
    path('transaction_group/add/', views.TransactionGroupAdd.as_view(), name='admin_transaction_group_add'),
    path('send_notification/', views.send_notification, name='admin_send_notification'),
    path('', views.Index.as_view(), name='admin_index'),
    path('charge/', views.ChargeCredit.as_view(), name='admin_charge'),
]
