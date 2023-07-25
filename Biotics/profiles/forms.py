from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from Biotics.profiles.models import BioticsUserModel


class BioticsUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = BioticsUserModel
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}),
    )
