from django import forms

from finance.models import BankPayment, FormPayment


class BankPaymentForm(forms.ModelForm):
    class Meta:
        model = BankPayment
        fields = ('amount', )


class ServicePaymentForm(forms.ModelForm):
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

    class Meta:
        model = FormPayment
        fields = (
            'first_name', 'last_name', 'phone_number',
            'security_number', 'passport_number',
            'exam_username', 'exam_password', 'exam_date', 'exam_country', 'exam_city', 'exam_center',
            'university_link', 'university_username', 'university_password',
            'amount',
        )
