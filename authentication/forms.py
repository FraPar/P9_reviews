from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
            model = get_user_model()
            fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
            widgets = {
                'username': forms.TextInput(attrs={'class' : "form-control"}),
                'email': forms.TextInput(attrs={'class' : "form-control"}),
                'first_name': forms.TextInput(attrs={'class' : "form-control"}),
                'last_name': forms.TextInput(attrs={'class' : "form-control"}),
                'password1': forms.TextInput(attrs={'class' : "form-control"}),
                'password2': forms.TextInput(attrs={'class' : "form-control"}),
            }
