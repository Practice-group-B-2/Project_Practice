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
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form__group',
            'placeholder': 'Введите ваше имя',
            'required': True
        }),
        help_text="Введите ваше имя"
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form__group',
            'placeholder': 'Введите вашу фамилию',
            'required': True
        }),
        help_text="Введите вашу фамилию"
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form__group',
            'placeholder': 'Придумайте имя пользователя',
            'required': True
        }),
        help_text="Придумайте уникальное имя пользователя"
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form__group',
            'placeholder': 'Введите ваш email',
            'required': True
        }),
        help_text="Введите ваш email"
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form__group',
            'placeholder': 'Придумайте пароль',
            'required': True
        }),
        help_text="Пароль должен содержать минимум 8 символов"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form__group',
            'placeholder': 'Повторите пароль',
            'required': True
        }),
        help_text="Повторите пароль для подтверждения"
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Согласен с условиями",
        widget=forms.CheckboxInput(attrs={'class': 'form__group'})
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()
        agree_to_terms = cleaned_data.get("agree_to_terms")

        if not agree_to_terms:
            self.add_error('agree_to_terms', "Вы должны согласиться с условиями для регистрации.")
        return cleaned_data




class InfoAbout(forms.Form):




    height = forms.IntegerField(
        min_value=100,
        max_value=250,
        label="Рост",
        help_text="Введите ваш рост в сантиметрах",
        widget=forms.NumberInput(attrs={'class': 'form__group'})
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=30,
        max_value=300,
        label="Вес",
        help_text="Введите ваш вес в килограммах",
        widget=forms.NumberInput(attrs={'class': 'form__group', 'step': '0.1'})
    )
    sickness = forms.ChoiceField(
        choices=UserProfile.SICKNESS_CHOICES,
        label="Заболевание",
        required=True,
        widget=forms.Select(attrs={'class': 'form__group'})
    )
    class Meta:
        model = User
        fields ={
            "height",
            "weight",
            "sickness",

        }
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.save(
                user=user,
                height=self.cleaned_data.get('height'),
                weight=self.cleaned_data.get('weight'),
                sickness=self.cleaned_data.get('sickness')
            )
        return user



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


