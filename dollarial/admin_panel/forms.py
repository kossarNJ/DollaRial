from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django import forms
from django.core.validators import MinValueValidator

from dollarial.models import Clerk, PaymentType, PaymentGroup

from finance.models import BankPayment


class ClerkCreateForm(forms.ModelForm):
    class Meta:
        model = Clerk
        fields = ("user", "salary", "is_employee")


class ClerkUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True

    class Meta:
        model = Clerk
        fields = ("user", "salary", "is_employee")


class PaymentGroupGeneralForm(forms.ModelForm):
    class Meta:
        model = PaymentGroup
        fields = ("name", )


class PaymentTypeGeneralForm(forms.ModelForm):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

    class Meta:
        model = PaymentType
        fields = ("name", "description", "fixed_price", "currency", "price", "max_amount", "min_amount",
                  "wage_percentage", "transaction_group", "required_fields", "is_active")


class BankPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.append(MinValueValidator(1))

    class Meta:
        model = BankPayment
        fields = ('amount', 'currency', )


class SendNotificationForm(forms.Form):
    subject = forms.CharField(required=True)
    notification_text = forms.CharField(required=True, widget=forms.Textarea)


class ReportForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=True, label="Comment")
