from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'content', 'placeholder': 'Логин *'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'content', 'placeholder': 'Пароль *'}))


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
       model = User
       fields = ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'password1', 'password2']
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'content', 'placeholder': 'Логин *'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'content', 'placeholder': 'Имя *'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'content', 'placeholder': 'Фамилия *'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'content', 'placeholder': 'Дата рождения *'}))
    gender = forms.CharField(widget=forms.TextInput(attrs={'class': 'content', 'placeholder': 'Пол *'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'content', 'placeholder': 'Пароль *'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'content', 'placeholder': 'Повторите пароль *'}))

