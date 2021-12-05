from django import forms
from .models import Image

class PostForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ['creator_profile', 'created_on']
