from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django import forms

from dollarial.models import Clerk, PaymentType


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


class PaymentTypeGeneralForm(forms.ModelForm):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

    class Meta:
        model = PaymentType
        fields = ("name", "description", "fixed_price", "currency", "price", "max_amount", "min_amount",
                  "wage_percentage", "transaction_group", "required_fields")
