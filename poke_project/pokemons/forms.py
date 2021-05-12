from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    """Formulario para crear nuevos usuarios"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
