from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # by default no email in form (but present in model User)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # what fields will be in form | they already are in model User