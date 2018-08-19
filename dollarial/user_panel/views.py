from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from dollarial.constants import TransactionConstants
from dollarial.models import PaymentType, get_dollarial_user
from finance import credit_manager
from finance.models import Exchange, BankPayment
from user_panel.forms import BankPaymentForm, ServicePaymentForm, InternalPaymentForm, ExternalPaymentForm, ExchangeForm
from dollarial.currency import *

def transaction_list(request):
    # TODO: read from db
    data = {
        "transactions": [
            {
                "id": "1",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user1",
                "destination": "Toefl Co.",
                "status": "reject"
            },
            {
                "id": "2",
                "transaction_type": "Gaj",
                "amount": "20000000000",
                "currency": "﷼",
                "owner": "user1",
                "destination": "Gaj Co.",
                "status": "unknown"
            },
            {
                "id": "3",
                "transaction_type": "IELTS",
                "amount": "100",
                "currency": "€",
                "owner": "user1",
                "destination": "Soroush Co.",
                "status": "accept"
            },
            {
                "id": "4",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user1",
                "destination": "Toefl Co.",
                "status": "reject"
            },
        ]
    }
    return render(request, 'user_panel/user_transaction_list.html', data)


def transaction_view(request, transaction_id):
    data = {
        "transaction": {
            "id": transaction_id,
            "transaction_type": "Toefl",
            "amount": "200",
            "currency": "$",
            "owner": "user1",
            "destination": "Toefl Co.",
            "status": "reject"
        }
    }
    return render(request, 'user_panel/user_transaction_view.html', data)


def edit_profile(request):
    data = {
        "user": {
            "fname": "kossar",
            "lname": "najafi",
            "email": "kossar.najafi@gmail.com",
            "phone": "09351234567"
        }
    }
    return render(request, 'user_panel/user_edit_profile.html', data)


def payment_form(request):
    return render(request, 'user_panel/payment_form.html')


class ServicePaymentConfirmation(LoginRequiredMixin, View):
    template_name = 'user_panel/service_payment_form_confirmation.html'
    form_class = ServicePaymentForm
    success_url = reverse_lazy('user_transaction_list')

    def get(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        redirect_respond = redirect('payment_form', payment_type_id)

        form_data_key = 'service_payment_form_data'
        if form_data_key not in request.session:
            return redirect_respond

        form_data = request.session.get(form_data_key)
        del request.session[form_data_key]
        form = self.form_class(payment_type, form_data)
        if not form.is_valid():
            return redirect_respond

        form.make_read_only()

        final_amount = form.cleaned_data.get('amount', payment_type.price)
        required_amount = final_amount / (1 - payment_type.wage_percentage / 100.0)
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = required_amount - final_amount

        data = {
            'form': form,
            'payment_type': payment_type,
            'final_amount':   final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        redirect_respond = redirect('payment_form', payment_type_id)

        form = self.form_class(payment_type, request.POST)
        if not form.is_valid():
            return redirect_respond

        payment_object = form.save(commit=False)
        payment_object.payment_type = payment_type
        payment_object.currency = payment_type.currency

        final_amount = payment_object.amount
        if payment_type.fixed_price:
            final_amount = payment_type.price
        final_amount = round(final_amount, 2)
        required_amount = final_amount / (1 - payment_type.wage_percentage / 100.0)
        required_amount = round(required_amount, 2)
        payment_object.wage = required_amount - final_amount
        payment_object.amount = required_amount
        payment_object.owner = request.user
        payment_object.status = 'I'
        payment_object.save()

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
            request.session['service_payment_form_data'] = form.cleaned_data
            return redirect('payment_form_confirmation', payment_type_id)
        data = {
            'form': form,
            'payment_type': payment_type
        }
        return render(request, self.template_name, data)


class InternalPayment(LoginRequiredMixin, View):
    form_class = InternalPaymentForm
    template_name = 'user_panel/user_internal_payment.html'
    success_url = reverse_lazy('user_transaction_list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            credit_manager.create_internal_payment(
                request.user,
                amount=form.cleaned_data['amount'],
                destination=form.cleaned_data['destination_account_number']
            )
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class ExternalPaymentConfirmation(LoginRequiredMixin, View):
    form_class = ExternalPaymentForm
    template_name = 'user_panel/user_external_payment_confirmation.html'
    success_url = reverse_lazy('user_transaction_list')

    @staticmethod
    def get_wage_percentage():
        return TransactionConstants.NORMAL_WAGE_PERCENTAGE

    def get(self, request, *args, **kwargs):
        redirect_respond = redirect('external_payment')

        form_data_key = 'external_payment_form'
        if form_data_key not in request.session:
            return redirect_respond

        form_data = request.session.get(form_data_key)
        del request.session[form_data_key]
        form = self.form_class(form_data)
        if not form.is_valid():
            return redirect_respond

        form.make_read_only()
        final_amount = form.cleaned_data.get('amount')
        required_amount = final_amount / (1 - self.get_wage_percentage() / 100.0)
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = required_amount - final_amount

        data = {
            'form': form,
            'currency_sign': Currency.get_by_char(form.cleaned_data['currency']).sign,
            'final_amount': final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        redirect_respond = redirect('external_payment')

        form = self.form_class(request.POST)
        if not form.is_valid():
            return redirect_respond

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
        payment_object.save()

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
        data = {
            "wallets": [
                {"name": currency.sign, "credit": request.user.get_credit(currency.char)}
                for currency in Currency.get_all_currencies()
            ]
        }
        return render(request, 'user_panel/user_index.html', data)


class ChargeCredit(LoginRequiredMixin, FormView):
    template_name = 'user_panel/user_charge.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('user_index')

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.currency = Currency.rial.char
        bank_payment.owner = self.request.user
        bank_payment.status = 'A'
        bank_payment.save()
        return super().form_valid(form)


class DepositCredit(LoginRequiredMixin, FormView):
    template_name = 'user_panel/user_deposit.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('user_index')

    def get(self, request, *args, **kwargs):
        print("there")
        form = self.form_class()
        data = {
            'form': form,
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        print("post")
        form = self.form_class(request.POST)
        if form.is_valid():
            bank_payment = form.save(commit=False)
            bank_payment.currency = Currency.rial.char
            bank_payment.owner = self.request.user
            bank_payment.amount *= -1
            bank_payment.status = 'A'

            print(self.request.user.get_credit(Currency.rial.char))
            print(-1*bank_payment.amount)

            if self.request.user.get_credit(Currency.rial.char) < (-1*bank_payment.amount):
                print("here")
                data = {
                    'form': form,
                    'is_error': 1
                }
                return render(request, self.template_name , data)

            bank_payment.save()
            data = {
                'form': form,
            }
            return render(request, 'user_panel/user_index.html', data)


class Services(LoginRequiredMixin, View):
    template_name = 'user_panel/user_services_list.html'

    def get(self, request, *args, **kwargs):
        available_services = PaymentType.objects\
            .filter(is_active=True)\
            .values('transaction_group', 'id')\
            .annotate(group_name=F('transaction_group__name'))\
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
    success_url = 'user_index'

    def get(self, request, *args, **kwargs):
        redirect_respond = redirect('user_exchange')

        form_data_key = 'exchange_data'
        if form_data_key not in request.session:
            return redirect_respond

        form_data = request.session.get(form_data_key)
        form = self.form_class(form_data)
        if not form.is_valid():
            return redirect_respond

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
        print(final_amount)
        required_amount = final_amount * (1 + TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        final_amount = round(final_amount, 2)
        required_amount = round(required_amount, 2)
        wage = final_amount * (TransactionConstants.NORMAL_WAGE_PERCENTAGE / 100.0) * sprice / fprice
        wage = round(wage, 2)

        if self.request.user.get_credit(fcur) < required_amount:
            print("error")
            print(required_amount)
            print(self.request.user.get_credit(fcur))
            print(fcur)
            exform = ExchangeForm()
            exdata = {
                'form': exform,
                'is_error': 1
            }
            return render(request, 'user_panel/user_exchange_credit.html', exdata)

        print("here")
        data = {
            'form': form,
            'final_amount':   final_amount,
            'required_amount': required_amount,
            'wage': wage,
        }
        return render(request, self.template_name, data)

    def post(self, request,*args, **kwargs):

        redirect_respond = redirect('user_exchange')

        form = self.form_class(request.POST)

        if not form.is_valid():
            return redirect_respond

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

        if self.request.user.get_credit(fcur) < required_amount:
            print("error")
            print(required_amount)
            print(self.request.user.get_credit(fcur))
            print(fcur)
            exform = ExchangeForm()
            exdata = {
                'form': exform,
                'is_error': 1
            }
            return render(request, 'user_panel/user_exchange_credit.html', exdata)


        bank_payment = BankPayment()
        bank_payment.currency = exchange_object.currency
        bank_payment.owner = self.request.user
        bank_payment.amount = -1 * required_amount
        bank_payment.status = 'A'
        bank_payment.save()

        bank_payment2 = BankPayment()
        bank_payment2.currency = exchange_object.currency
        bank_payment2.owner = get_dollarial_user()
        bank_payment2.amount = wage
        bank_payment2.status = 'A'
        bank_payment2.save()

        bank_payment3 = BankPayment()
        bank_payment3.currency = exchange_object.final_currency
        bank_payment3.owner = self.request.user
        bank_payment3.amount = final_amount
        bank_payment3.status = 'A'
        bank_payment3.save()

        return redirect(self.success_url)


class Exchange(LoginRequiredMixin, View):

    model = Exchange
    template_name = 'user_panel/user_exchange_credit.html'
    success_url = reverse_lazy('user_panel/user_index.html')
    form_class = ExchangeForm
    success_url = 'user_index'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        data = {
            'form': form,
            'is_error': 0
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['exchange_data'] = form.cleaned_data
            return redirect('user_exchange_accept')

        data = {
            'form': form,
            'is_error': 0
        }
        return render(request, self.template_name, data)
