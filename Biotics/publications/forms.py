from django import forms

from Biotics.publications.models import PublicationModel, Comment


class PublicationCreateForm(forms.ModelForm):
    class Meta:
        model = PublicationModel
        fields = '__all__'
        exclude = {'user', 'likes_count'}


class PublicationEditForm(forms.ModelForm):
    class Meta:
        model = PublicationModel
        exclude = ['photo', 'user', 'likes_count']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Add comment...'
                }
            )
        }
