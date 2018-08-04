from django import forms

from dollarial.models import Clerk


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
