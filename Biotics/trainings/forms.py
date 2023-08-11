from django import forms

from Biotics.trainings.models import TrainingModel


class TrainingCreateForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        fields = '__all__'
        exclude = {'user', 'price'}


class TrainingEditForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        exclude = ['training', 'user']

