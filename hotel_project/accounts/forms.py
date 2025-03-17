from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm): # Клас каторый содержит встроеную форму имя и пароль
    email = forms.EmailField(required=True)  # Добовляем еще одну форму уже в готовую с именим и поролем

    class Meta: # Указываем что наша форма будет работать с БД
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Определения спика полей в БД