# documents/forms.py
from django import forms
from .models import Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
