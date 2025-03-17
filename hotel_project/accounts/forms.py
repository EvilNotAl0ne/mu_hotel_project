from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm): # Класс каторый содержит встроеную форму имя и пароль
    email = forms.EmailField(required=True)  # Добовляем еще одну форму уже в готовую с именим и поролем

    class Meta: # Указываем что наша форма будет работать с БД
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Определения спика полей в БД

class LoginForm(AuthenticationForm): # Класс каторый содержит встроеную форму аунтефикации
    username = forms.CharField(
        label="Имя пользователя", # Отоброжает надпись рядом с полем ввода
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}) # TextInput то что это текстовое поле
    )
    password = forms.CharField(
        label="Пароль",  # Отоброжает надпись рядом с полем ввода
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})  # PasswordInput то что это текстовое поле ввода пороля
    )


