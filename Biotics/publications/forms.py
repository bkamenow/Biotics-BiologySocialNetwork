from django import forms

from Biotics.publications.models import PublicationModel


class PublicationCreateForm(forms.ModelForm):
    class Meta:
        model = PublicationModel
        fields = '__all__'
        exclude = {'user'}
