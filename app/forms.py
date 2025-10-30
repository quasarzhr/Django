from django import forms
from .models import Post

class ContactForm(forms.Form):
    """Basic contact form for validation test"""
    name = forms.CharField(max_length=50)
    email = forms.EmailField()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']