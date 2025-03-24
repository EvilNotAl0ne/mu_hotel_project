from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm): # Класс каторый содержит встроеную форму имя и пароль
    email = forms.EmailField(required=True)  # Добовляем еще одну форму уже в готовую с именим и поролем

    class Meta: # Указываем что наша форма будет работать с БД
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Определения спика полей в БД

class LoginForm(AuthenticationForm): # Класс в котором содержит встроенную форму аунтефикации
    username = forms.CharField(
        label="Имя пользователя", # Отображает надпись рядом с полем ввода
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}) # TextInput то что это текстовое поле
    )
    password = forms.CharField(
        label="Пароль",  # Отображает надпись рядом с полем ввода
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})  # PasswordInput то что это текстовое поле ввода пороля
    )


class UserUpdateForm(forms.ModelForm):  # Класс которы содержит встроенную форму User (username и email)
    class Meta:  # Класс для настройки формы
        model = User  #  Указываем что работаем с моделью User
        fields = ['username', 'email']  # Перечисляем поля с которыми будем работать

class ProfileUpdateForm(forms.ModelForm):  # То же самое
    class Meta:  # То же самое
        model = Profile  # Указываем что работаем с моделью Profile
        fields = [   # Перечисляем поля с которыми будем работать
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'passport_data'
        ]

