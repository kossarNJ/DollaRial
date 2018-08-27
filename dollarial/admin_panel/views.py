from collections import OrderedDict

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django import urls
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView

from admin_panel.models import ReportTransaction, ReviewHistory
from admin_panel.review import review_transaction
from dollarial.currency import Currency
from dollarial.mixins import ClerkRequiredMixin, StaffRequiredMixin
from dollarial.models import User, Clerk, get_dollarial_company, get_dollarial_user, PaymentType, PaymentGroup

from django.views.generic import FormView
from django.shortcuts import render, redirect

from dollarial import notification
from finance.models import Transaction
from . import forms
from admin_panel.forms import BankPaymentForm, SendNotificationForm

import requests


class TransactionList(ClerkRequiredMixin, ListView):
    model = Transaction
    template_name = 'admin_panel/admin_transaction_list.html'
    ordering = ['-id']


class TransactionView(ClerkRequiredMixin, View):
    report_form_class = forms.ReportForm

    def get(self, request, transaction_id, *args, **kwargs):
        transaction = Transaction.objects.get(id=transaction_id)
        report_form = self.report_form_class()
        data = {
            "transaction": transaction,
            "display_fields": OrderedDict(transaction.get_display_data()),
            "report_form": report_form,
            "reports": ReportTransaction.objects.filter(transaction_id=transaction_id).order_by('-time'),
            "reviewable": transaction.status == 'I' or request.user.is_staff
        }
        return render(request, 'admin_panel/admin_transaction_view.html', data)

    def post(self, request, transaction_id, *args, **kwargs):
        success_redirect = redirect('admin_transaction_view', transaction_id)

        transaction = Transaction.objects.get(id=transaction_id)
        if 'comment' in request.POST:
            report_form = self.report_form_class(request.POST)
            if report_form.is_valid():
                report_object = ReportTransaction(
                    reviewer=request.user,
                    comment=report_form.cleaned_data['comment'],
                    transaction=transaction
                )
                report_object.save()
                messages.add_message(request, messages.SUCCESS, "Your report is sent to the admin.")
        else:
            if not request.user.is_staff and transaction.status != 'I':
                messages.add_message(request, messages.ERROR, 'This transaction is reviewed before.')
                return success_redirect
            try:
                pre_status = transaction.status
                review_transaction(request, transaction)
                post_status = transaction.status
                if pre_status != post_status:
                    notification.send_notification_to_user(
                        request.user,
                        subject='#%d Transaction Review Result' % transaction_id,
                        message='Your transaction is reviewed and the result is %s.\nLink: %s' %
                                (transaction.get_status_display(),
                                 urls.reverse('user_transaction_view', args=[transaction_id]))
                    )
                messages.add_message(request, messages.SUCCESS, "Your action is received.")
            except ValueError as err:
                print("Error: %s" % err)

        return success_redirect


class UserList(ClerkRequiredMixin, ListView):
    model = User
    template_name = 'admin_panel/admin_costumer_list.html'


class UserUpdate(ClerkRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'admin_panel/admin_costumer_view.html'
    fields = ['username', 'first_name', 'last_name', 'account_number', 'email', 'phone_number',
              'is_active', 'is_staff']
    success_url = reverse_lazy('admin_costumer_list')
    success_message = "User profile is updated successfully."


class ClerkList(StaffRequiredMixin, ListView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_list.html'


class ClerkAdd(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_add.html'
    success_url = reverse_lazy('admin_reviewer_list')
    success_message = "A new Clerk is added successfully."
    form_class = forms.ClerkCreateForm


class ClerkUpdate(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_view.html'
    success_url = reverse_lazy('admin_reviewer_list')
    success_message = "Clerk profile is updated successfully."
    form_class = forms.ClerkUpdateForm


class PaymentTypeAdd(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_add.html'
    success_url = reverse_lazy('admin_transaction_type_list')
    success_message = "Payment Type is added successfully."
    form_class = forms.PaymentTypeGeneralForm


class PaymentTypeList(StaffRequiredMixin, ListView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_list.html'


class PaymentTypeView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_view.html'
    success_url = reverse_lazy('admin_transaction_type_list')
    success_message = "Payment Type is updated successfully."
    form_class = forms.PaymentTypeGeneralForm


class SkippedTransactionsHistory(StaffRequiredMixin, ListView):
    model = ReviewHistory
    template_name = 'admin_panel/admin_skipped_transaction_list.html'

    def get_queryset(self):
        return self.model.objects.filter(action='S')


class ReviewedTransactionsHistory(ClerkRequiredMixin, ListView):
    model = ReviewHistory
    template_name = 'admin_panel/admin_reviewed_transaction_list.html'

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            query_set = self.model.objects.filter(reviewer_id=user.id)
        else:
            query_set = self.model.objects.filter(action__in=['R', 'A'])
        return query_set


class ReportList(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/admin_reports_list.html'
    model = ReportTransaction


class TransactionGroupList(StaffRequiredMixin, ListView):
    model = PaymentGroup
    template_name = 'admin_panel/admin_transaction_group_list.html'


class TransactionGroupView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PaymentGroup
    template_name = 'admin_panel/admin_transaction_group_view.html'
    fields = ('name',)
    success_url = reverse_lazy('admin_transaction_group_list')
    success_message = "Payment Group successfully updated."


class TransactionGroupAdd(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = PaymentGroup
    template_name = 'admin_panel/admin_transaction_group_add.html'
    fields = ('name',)
    success_url = reverse_lazy('admin_transaction_group_list')
    success_message = "Payment Group successfully added."


@staff_member_required
def send_notification(request):
    if request.method == 'GET':
        form = SendNotificationForm()
    else:
        form = SendNotificationForm(request.POST)
        if "cancel" in request.POST:
            return redirect('admin_index')
        else:
            if form.is_valid():
                message = form.cleaned_data['notification_text']
                subject = form.cleaned_data['subject']

                data = {
                    "app_id": "c414492c-f6ce-4c68-8691-d9192102118a",
                    "included_segments": ["All"],
                    "contents": {"en": subject + ":  " + message}
                }
                requests.post(
                    "https://onesignal.com/api/v1/notifications",
                    headers={"Authorization": "Basic MWJjY2FkZDMtNzc0Mi00MDBhLTlkYzQtMjIzZGY2MDVmZjZj"},
                    json=data
                )

                return redirect('admin_index')
    return render(request, "admin_panel/admin_send_notification.html", {'form': form})


class Index(ClerkRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "wallets": [
                {"name": currency.sign, "credit": get_dollarial_company().get_credit(currency.char)}
                for currency in Currency.get_all_currencies()
            ]
        }
        return render(request, 'admin_panel/admin_index.html', data)


class ChargeCredit(StaffRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'admin_panel/admin_charge.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('admin_index')
    success_message = "You charged company's wallet successfully!"

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.owner = get_dollarial_user()
        bank_payment.status = 'A'
        bank_payment.save()
        return super().form_valid(form)
