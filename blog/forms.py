from django import forms
from .models import Comment 

class FormComment(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['name','email','text']