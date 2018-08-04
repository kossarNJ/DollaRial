from django import forms

from finance.models import BankPayment


class BankPaymentForm(forms.ModelForm):
    class Meta:
        model = BankPayment
        fields = ('amount', )
