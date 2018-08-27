from collections import defaultdict, OrderedDict
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, ListView

from user_panel.forms import UserUpdateForm
from dollarial.constants import TransactionConstants
from dollarial.models import PaymentType, User
from finance import credit_manager
from finance.models import Exchange, BankPayment, Transaction
from user_panel.forms import BankPaymentForm, ServicePaymentForm, InternalPaymentForm, ExternalPaymentForm, ExchangeForm
from dollarial.currency import *


@login_required
def get_wallets_context_data(request):
    return {
        "wallets": [
            {
                "name": currency.sign,
                "credit": request.user.get_credit(currency.char)
            } for currency in Currency.get_all_currencies()
        ]
    }


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'user_panel/user_transaction_list.html'

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user).order_by('-time')


class TransactionView(LoginRequiredMixin, View):
    template_name = 'user_panel/user_transaction_view.html'

    def get(self, request, transaction_id, *args, **kwargs):
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.owner != request.user:
            return HttpResponseForbidden()

        display_fields = OrderedDict(transaction.get_display_data())

        data = {
            "transaction": transaction,
            "display_fields": display_fields,
        }
        return render(request, self.template_name, data)


class ServicePaymentConfirmation(LoginRequiredMixin, View):
    template_name = 'user_panel/service_payment_form_confirmation.html'
    form_class = ServicePaymentForm
    success_url = reverse_lazy('user_transaction_list')

    def __respond_in_error(self, payment_type_id, error_message='Something went wrong'):
        redirect_respond = redirect('payment_form', payment_type_id)
        messages.add_message(self.request, messages.ERROR, error_message)
        return redirect_respond

    def get(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)

        form_data_key = 'service_payment_form_data'
        if form_data_key not in request.session:
            return self.__respond_in_error(payment_type_id)

        form_data = request.session.get(form_data_key)
        if 'exam_date' in form_data:
            form_data['exam_date'] = datetime.datetime.strptime(form_data['exam_date'], "%Y-%m-%d")
        del request.session[form_data_key]
        form = self.form_class(payment_type, form_data)
        if not form.is_valid():
            return self.__respond_in_error(payment_type_id)

        form.make_read_only()

        final_amount = form.cleaned_data.get('amount', payment_type.price)
        currency = payment_type.currency
        required_amount = final_amount / (1 - payment_type.wage_percentage / 100.0)
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = required_amount - final_amount

        if not credit_manager.check_enough_credit(required_amount, currency, request.user):
            return self.__respond_in_error(payment_type_id, "Not enough credit.")

        data = {
            'form': form,
            'payment_type': payment_type,
            'final_amount': final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)

        form = self.form_class(payment_type, request.POST)
        if not form.is_valid():
            return self.__respond_in_error(payment_type_id)

        payment_object = form.save(commit=False)
        payment_object.payment_type = payment_type
        payment_object.currency = payment_type.currency

        if payment_type.fixed_price:
            final_amount = payment_type.price
        else:
            final_amount = payment_object.amount

        final_amount = round(final_amount, 2)
        required_amount = final_amount / (1 - payment_type.wage_percentage / 100.0)
        required_amount = round(required_amount, 2)
        payment_object.wage = required_amount - final_amount
        payment_object.amount = required_amount
        payment_object.owner = request.user
        payment_object.status = 'I'

        with transaction.atomic():
            if credit_manager.check_validity_of_new_transaction(payment_object):
                payment_object.save()
            else:
                return self.__respond_in_error(payment_type_id, "Not enough credit.")

        return redirect(self.success_url)


class ServicePayment(LoginRequiredMixin, View):
    form_class = ServicePaymentForm
    template_name = 'user_panel/service_payment_form.html'

    def get(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        form = self.form_class(payment_type)
        data = {
            'form': form,
            'payment_type': payment_type
        }
        return render(request, self.template_name, data)

    def post(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        form = self.form_class(payment_type, request.POST)
        if form.is_valid():
            data_to_session = form.cleaned_data
            for key, value in data_to_session.items():
                if isinstance(value, datetime.date):
                    data_to_session[key] = value.strftime('%Y-%m-%d')
            request.session['service_payment_form_data'] = data_to_session
            return redirect('payment_form_confirmation', payment_type_id)
        else:
            print('form is not valid')

        data = {
            'form': form,
            'payment_type': payment_type
        }
        return render(request, self.template_name, data)


class InternalPayment(LoginRequiredMixin, View):
    form_class = InternalPaymentForm
    template_name = 'user_panel/user_internal_payment.html'
    success_url = reverse_lazy('user_transaction_list')
    success_message = "Internal payment submitted successfully."

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            owner = request.user

            if credit_manager.check_enough_credit(amount, currency='R', user=owner):
                credit_manager.create_internal_payment(
                    owner,
                    amount=amount,
                    destination=form.cleaned_data['destination_account_number']
                )
                messages.add_message(request, level=messages.SUCCESS, message=self.success_message)
                return redirect(self.success_url)
            else:
                messages.add_message(request, level=messages.ERROR, message="Not enough credit")

        return render(request, self.template_name, {'form': form})


class ExternalPaymentConfirmation(LoginRequiredMixin, View):
    form_class = ExternalPaymentForm
    template_name = 'user_panel/user_external_payment_confirmation.html'
    success_url = reverse_lazy('user_transaction_list')
    success_message = "External payment submitted successfully.\nPlease wait till we review your request."

    @staticmethod
    def get_wage_percentage():
        return TransactionConstants.NORMAL_WAGE_PERCENTAGE

    def __respond_in_error(self, error_message='Something went wrong'):
        redirect_respond = redirect('external_payment')
        messages.add_message(self.request, messages.ERROR, error_message)
        return redirect_respond

    def get(self, request, *args, **kwargs):
        form_data_key = 'external_payment_form'
        if form_data_key not in request.session:
            return self.__respond_in_error()

        form_data = request.session.get(form_data_key)
        del request.session[form_data_key]
        form = self.form_class(form_data)
        if not form.is_valid():
            return self.__respond_in_error()
        form.make_read_only()

        currency = form.cleaned_data['currency']
        final_amount = form.cleaned_data.get('amount')
        required_amount = final_amount / (1 - self.get_wage_percentage() / 100.0)
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = required_amount - final_amount

        if not credit_manager.check_enough_credit(required_amount, currency, request.user):
            return self.__respond_in_error("Not enough credit.")

        data = {
            'form': form,
            'currency_sign': Currency.get_by_char(form.cleaned_data['currency']).sign,
            'final_amount': final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self.__respond_in_error()

        payment_object = form.save(commit=False)
        payment_object.owner = request.user
        final_amount = payment_object.amount
        final_amount = round(final_amount, 2)
        required_amount = final_amount / (1 - self.get_wage_percentage() / 100.0)
        required_amount = round(required_amount, 2)
        payment_object.wage = required_amount - final_amount
        payment_object.amount = -required_amount
        payment_object.owner = request.user
        payment_object.status = 'I'

        with transaction.atomic():
            if credit_manager.check_validity_of_new_transaction(payment_object):
                payment_object.save()
            else:
                return self.__respond_in_error("Not enough credit.")

        messages.add_message(request, level=messages.SUCCESS, message=self.success_message)
        return redirect(self.success_url)


class ExternalPayment(LoginRequiredMixin, FormView):
    template_name = 'user_panel/user_external_payment.html'
    form_class = ExternalPaymentForm
    success_url = reverse_lazy('external_payment_confirmation')

    def form_valid(self, form):
        self.request.session['external_payment_form'] = form.cleaned_data
        return super().form_valid(form)


class Index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = get_wallets_context_data(request)
        return render(request, 'user_panel/user_index.html', data)


class ChargeCredit(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'user_panel/user_charge.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('user_index')
    success_message = "Wallet is charged successfully."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(get_wallets_context_data(request=self.request))
        return data

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.currency = Currency.rial.char
        bank_payment.owner = self.request.user
        bank_payment.status = 'A'
        bank_payment.save()
        return super().form_valid(form)


class DepositCredit(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'user_panel/user_deposit.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('user_index')
    success_message = "Your deposit request is submitted successfully.\nPlease wait till we review your request."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(get_wallets_context_data(request=self.request))
        return data

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.currency = Currency.rial.char
        bank_payment.owner = self.request.user
        bank_payment.amount *= -1
        bank_payment.status = 'I'

        with transaction.atomic():
            if credit_manager.check_validity_of_new_transaction(bank_payment):
                bank_payment.save()
            else:
                messages.add_message(self.request, messages.ERROR, "Not enough credit.")
                return render(self.request, self.template_name, self.get_context_data())

        return super().form_valid(form)


class Services(LoginRequiredMixin, View):
    template_name = 'user_panel/user_services_list.html'

    def get(self, request, *args, **kwargs):
        available_services = PaymentType.objects \
            .filter(is_active=True) \
            .values('transaction_group', 'id') \
            .annotate(group_name=F('transaction_group__name')) \
            .values_list('group_name', 'id', 'name', 'description', named=True)
        services = defaultdict(list)
        for row in available_services:
            services[row.group_name].append(row)
        data = {
            "service_groups": dict(services)
        }
        return render(request, self.template_name, data)


class ExchangeConfirmation(LoginRequiredMixin, View):
    template_name = 'user_panel/user_exchange_acceptance.html'
    form_class = ExchangeForm
    success_url = reverse_lazy('user_index')
    fail_url = reverse_lazy('user_exchange')

    @staticmethod
    def __respond_in_error(request, error_message='Something went wrong'):
        redirect_respond = redirect('user_exchange')
        messages.add_message(request, messages.ERROR, error_message)
        return redirect_respond

    def get(self, request, *args, **kwargs):
        form_data_key = 'exchange_data'
        if form_data_key not in request.session:
            return self.__respond_in_error(request)
        form_data = request.session.get(form_data_key)
        del request.session[form_data_key]
        form = self.form_class(form_data)
        if not form.is_valid():
            return self.__respond_in_error(request)

        form.make_read_only()

        fcur = form.cleaned_data.get('currency')
        scur = form.cleaned_data.get('final_currency')
        fprice = 1
        sprice = 1

        if fcur == 'D':
            fprice = get_dollar_rial_value()
        if fcur == 'E':
            fprice = get_euro_rial_value()
        if scur == 'D':
            sprice = get_dollar_rial_value()
        if scur == 'E':
            sprice = get_euro_rial_value()

        final_amount = form.cleaned_data.get('final_amount')

        required_amount = final_amount * (1 + TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = final_amount * (TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        wage = round(wage, 2)

        if not credit_manager.check_enough_credit(required_amount, fcur, request.user):
            return self.__respond_in_error(request, error_message="Not enough credit.")

        data = {
            'form': form,
            'final_amount': final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.__respond_in_error(request)

        exchange_object = form.save(commit=False)

        fcur = exchange_object.currency
        scur = exchange_object.final_currency
        fprice = 1
        sprice = 1

        if fcur == 'D':
            fprice = get_dollar_rial_value()
        if fcur == 'E':
            fprice = get_euro_rial_value()
        if scur == 'D':
            sprice = get_dollar_rial_value()
        if scur == 'E':
            sprice = get_euro_rial_value()

        final_amount = exchange_object.final_amount
        required_amount = final_amount * (1 + TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = final_amount * (TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        wage = round(wage, 2)

        with transaction.atomic():
            if credit_manager.check_enough_credit(required_amount, fcur, request.user):
                bank_payment = BankPayment()
                bank_payment.currency = exchange_object.currency
                bank_payment.owner = self.request.user
                bank_payment.amount = -1 * required_amount
                bank_payment.status = 'A'
                bank_payment.wage = wage
                bank_payment.save()

                bank_payment2 = BankPayment()
                bank_payment2.currency = exchange_object.final_currency
                bank_payment2.owner = self.request.user
                bank_payment2.amount = final_amount
                bank_payment2.status = 'A'
                bank_payment2.save()
            else:
                return self.__respond_in_error(request, error_message="Not enough credit.")

        messages.add_message(self.request, messages.SUCCESS, "You exchanged your money successfully.")
        return redirect(self.success_url)


class ExchangeView(LoginRequiredMixin, View):
    model = Exchange
    template_name = 'user_panel/user_exchange_credit.html'
    form_class = ExchangeForm

    def get_default_data(self):
        return get_wallets_context_data(request=self.request)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        data = {
            'form': form,
        }
        data.update(self.get_default_data())
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['exchange_data'] = form.cleaned_data
            return redirect('user_exchange_accept')

        data = {
            'form': form,
        }
        data.update(self.get_default_data())
        return render(request, self.template_name, data)


class ProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'user_panel/user_edit_profile.html'
    success_url = reverse_lazy('user_edit_profile')
    success_message = "Profile successfully updated!"
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.user.id)
        return obj
