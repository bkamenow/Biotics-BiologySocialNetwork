from django import forms

from Biotics.publications.models import PublicationModel, Comment


class PublicationCreateForm(forms.ModelForm):
    class Meta:
        model = PublicationModel
        fields = '__all__'
        exclude = {'user'}


class PublicationEditForm(forms.ModelForm):
    class Meta:
        model = PublicationModel
        exclude = ['publication', 'user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Add comment...'
                }
            )
        }