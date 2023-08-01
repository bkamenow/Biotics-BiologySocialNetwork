from django import forms

from Biotics.trainings.models import TrainingModel


class TrainingCreateForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        fields = '__all__'
        exclude = {'user'}


class TrainingEditForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        exclude = ['training', 'user']


class PaymentForm(forms.Form):
    credit_card_number = forms.CharField(label='Credit Card Number',
                                         widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    expiration_date = forms.CharField(label='Expiration Date', widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cardholder_name = forms.CharField(label='Cardholder Name',
                                      widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    security_code = forms.CharField(label='Security Code (CVV/CVC)',
                                    widget=forms.TextInput(attrs={'placeholder': '123'}))
    billing_address = forms.CharField(label='Billing Address', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    stripe_token = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit_card_number'].widget.attrs['maxlength'] = 19
        self.fields['expiration_date'].widget.attrs['maxlength'] = 5
        self.fields['security_code'].widget.attrs['maxlength'] = 4
