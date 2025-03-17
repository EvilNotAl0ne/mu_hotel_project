from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# authenticate - проверяет существует ли такой пользователь
# login - остовляет аутефецированым пользователя
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':  # Проверяем был ли POST запрос
        form = RegisterForm(request.POST)
        if form.is_valid():  # Проверяем была ли коректно заполнена наша форма
            user = form.save()  # Если все ок, то сохраняем
            login(request, user)  # Если так же все ок, то авторизуем пользователя
            return redirect('home') # И перемещаем его на главную страницу

    else:
        form = RegisterForm() # Если метод GET, то просто отображаем пустую форму для заполнения

    return render(request, 'accounts/register.html', {'form': form})  # Это путь к нашему шаблону HTML для отображения визуального вида нашей формы


def user_login(request):
    if request.method == 'POST':  # Проверяет заполнена ли форма да или нет
        form = LoginForm(request, data=request.POST)  # Если да, то заполняет нашу форму
        if form.is_valid():        # Проверяет валидацию, все ли прошло, все ли заполнено
            username = form.cleaned_data['username']  # Если все ок, то извлекает наши запоненые данные
            password = form.cleaned_data['password']  # Тут то же самое!
            user = authenticate(request, username=username, password=password) # Функция authenticate проверяет если такой пользователь, если да то возвращает его, если нет то возвращает None
            if user is not None:  # Если пользователь Не равен None
                login(request, user) # То авторизует его
                return redirect('home') # И отправляет его на главную страницу

    else:
        form = LoginForm()  # Если метод GET, то просто отображаем пустую форму для заполнения

    return render(request, 'accounts/login.html', {'form': form})  # Это путь к нашему шаблону HTML для отображения визуального вида нашей формы
