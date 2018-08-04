from django.contrib.auth.forms import UserCreationForm

from dollarial.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'password1', 'password2', 'account_number', 'notification_preference')
