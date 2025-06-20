from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

from .models import *
from django.forms import ModelForm

Sickness_CHOICES = (
    ('Sugar Diabat', 'Сахарный диабет'),
    ('Celiac disease', 'Целиакия'),
    ('Phenylketonuria', 'Фенилкетонурия'),
)

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    agree_to_terms = forms.BooleanField(required=True, label="Согласен с условиями")
    height = forms.IntegerField(
        min_value=100,
        max_value=250,
        label="Рост",
        help_text="Введите ваш рост в сантиметрах",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=30,
        max_value=300,
        label="Вес",
        help_text="Введите ваш вес в килограммах",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    sickness = forms.ChoiceField(
        choices=UserProfile.SICKNESS_CHOICES,
        label="Заболевание",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "height",
            "weight",
            "sickness",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                height=self.cleaned_data.get('height'),
                weight=self.cleaned_data.get('weight'),
                sickness=self.cleaned_data.get('sickness')
            )
        return user

    def clean(self):
        cleaned_data = super().clean()
        agree_to_terms = cleaned_data.get("agree_to_terms")

        if not agree_to_terms:
            self.add_error('agree_to_terms', "Вы должны согласиться с условиями для регистрации.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


