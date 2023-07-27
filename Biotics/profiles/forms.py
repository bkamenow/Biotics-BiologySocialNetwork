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


class BioticsUserEditForm(forms.ModelForm):
    class Meta:
        model = BioticsUserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture', 'gender', 'biology_type', 'rank')
        exclude = ('password',)
        labels = {
            'username': 'Username:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'email': 'Email:',
            'profile_picture': 'Image:',
            'gender': 'Gender:',
            'age': 'Age:',
            'biology_type': 'Biology type:',
            'rank': 'Rank:',
        }
        