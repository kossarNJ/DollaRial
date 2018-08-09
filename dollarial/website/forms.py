from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)
