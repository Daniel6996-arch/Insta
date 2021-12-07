from django import forms
from .models import Image, Comment

class PostForm(forms.ModelForm):
    image = forms.FileField(label='Upload image') 

    class Meta:
        model = Image
        exclude = ['author', 'created_on', 'likes', 'dislikes']


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
