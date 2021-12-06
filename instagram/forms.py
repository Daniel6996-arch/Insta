from django import forms
from .models import Image, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ['creator_profile', 'created_on']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs={
            'rows': '3',
            'placeholder':'Comment Something...'
        })   
    )

    class Meta:
        model = Comment
        fields = ['comment']
