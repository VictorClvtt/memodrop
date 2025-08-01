from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from . import models

class RegisterUser(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        