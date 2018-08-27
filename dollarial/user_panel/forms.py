from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from dollarial.constants import TransactionConstants
from dollarial.fields import PriceFormField
from finance.models import BankPayment, FormPayment, Exchange, ExternalPayment
from dollarial.models import User


class ExchangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].label = "First Wallet"
        self.fields['final_amount'].label = "Amount to Target Wallet"
        self.fields['final_currency'].label = "Target Wallet"
        self.fields['final_amount'].validators.extend([
            MinValueValidator(TransactionConstants.MIN_EXCHANGE_FINAL_AMOUNT),
            MaxValueValidator(TransactionConstants.MAX_EXCHANGE_FINAL_AMOUNT)
        ])

    def make_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Exchange
        fields = ('final_currency', 'final_amount', 'currency',)


class BankPaymentForm(forms.ModelForm):
    def __init__(self, charge_form=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.append(MinValueValidator(TransactionConstants.MIN_CHARGE_DEPOSIT_AMOUNT))
        if charge_form:
            self.fields['amount'].validators.append(MaxValueValidator(TransactionConstants.MAX_CHARGE_AMOUNT))

    class Meta:
        model = BankPayment
        fields = ('amount',)


class ExternalPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.extend([
            MinValueValidator(TransactionConstants.MIN_EXTERNAL_PAYMENT_AMOUNT),
            MaxValueValidator(TransactionConstants.MAX_EXTERNAL_PAYMENT_AMOUNT)
        ])

    def make_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = ExternalPayment
        fields = ('amount', 'destination_number', 'currency',)


class InternalPaymentForm(forms.Form):
    amount = PriceFormField(label="Amount (in ﷼)")
    destination_account_number = forms.CharField(max_length=32, label="Destination Account Number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.extend([
            MinValueValidator(TransactionConstants.MIN_INTERNAL_PAYMENT_AMOUNT),
            MaxValueValidator(TransactionConstants.MAX_INTERNAL_PAYMENT_AMOUNT)
        ])


class ServicePaymentForm(forms.ModelForm):
    error_css_class = "error"

    def __init__(self, payment_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for flag, value in payment_type.required_fields:
            for field in FormPayment.flag_related_fields[flag]:
                if value:
                    self.fields[field].required = True
                else:
                    del self.fields[field]
        if payment_type.fixed_price:
            del self.fields['amount']
        else:
            self.fields['amount'].validators.extend([
                MinValueValidator(payment_type.min_amount),
                MaxValueValidator(payment_type.max_amount),
            ])
        for field in self.fields:
            if isinstance(self.fields[field], forms.DateField):
                self.fields[field].widget.attrs['class'] = 'datepicker'

    def make_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = FormPayment
        fields = (
            'first_name', 'last_name', 'phone_number',
            'security_number', 'passport_number',
            'exam_username', 'exam_password', 'exam_date', 'exam_country', 'exam_city', 'exam_center',
            'university_link', 'university_username', 'university_password',
            'amount',
        )


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'notification_preference']
