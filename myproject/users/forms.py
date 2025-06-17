from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserChangePasswordForm(forms.Form):
    need_generate = forms.BooleanField()
    email = forms.EmailField(required=True)
