from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from django.forms import ModelForm



class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    agree_to_terms = forms.BooleanField(required=True, label="Согласен с условиями")
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  )

    def clean(self):
        cleaned_data = super().clean()
        agree_to_terms = cleaned_data.get("agree_to_terms")

        if not agree_to_terms:
            self.add_error('agree_to_terms', "Вы должны согласиться с условиями для регистрации.")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


