from collections import defaultdict
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from dollarial.currency import Currency
from dollarial.models import PaymentType
from user_panel.forms import BankPaymentForm, ServicePaymentForm


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
    success_url = 'user_transaction_list'

    def get(self, request, payment_type_id, *args, **kwargs):
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        redirect_respond = redirect('payment_form', payment_type_id)

        form_data_key = 'service_payment_form_data'
        if form_data_key not in request.session:
            return redirect_respond

        form_data = request.session.get(form_data_key)
        # del request.session[form_data_key]
        form = self.form_class(payment_type, form_data)
        if not form.is_valid():
            return redirect_respond

        form.make_read_only()

        final_amount = form.cleaned_data.get('amount', payment_type.price)
        required_amount = final_amount / (1 - payment_type.wage_percentage / Decimal(100.0))
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
        required_amount = final_amount / (1 - payment_type.wage_percentage / Decimal(100.0))
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


def payment_result(request):
    data = {
        "transaction": {
            "transaction_type": "University",
            "amount": "200",
            "currency": "$",
            "destination": "Stanford University",
        }
    }
    return render(request, 'user_panel/payment_result.html', data)


def exchange(request):
    data = {
        "wallets": {
            "rial": {
                "credit": 1000,
            },
            "dollar": {
                "credit": 2200,
            },
            "euro": {
                "credit": 1020
            }
        }
    }
    return render(request, 'user_panel/user_exchange_credit.html', data)


def exchange_accept(request):
    data = {
        "currencies": [
            "rial", "dollar", "euro"
        ],
        "from": "dollar",
        "to": "rial",
        "amount": {
            "from": 1,
            "to": 75000 * 0.93,
            "wage": 75000 * 0.07,
        }
    }
    return render(request, 'user_panel/user_exchange_acceptance.html', data)


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

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.currency = Currency.rial.char
        bank_payment.owner = self.request.user
        bank_payment.amount *= -1
        bank_payment.status = 'A'
        bank_payment.save()
        return super().form_valid(form)


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
