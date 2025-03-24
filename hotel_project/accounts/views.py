from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
# authenticate - проверяет существует ли такой пользователь
# login - остовляет аутефецированым пользователя
from .forms import RegisterForm, LoginForm
from main.models import Booking

def register(request):
    if request.method == 'POST':  # Проверяем был ли POST запрос
        form = RegisterForm(request.POST)
        if form.is_valid():  # Проверяем была ли коректно заполнена наша форма
            user = form.save()  # Если все ок, то сохраняем
            login(request, user)  # Если так же все ок, то авторизуем пользователя
            return redirect('home')  # И перемещаем его на главную страницу

    else:
        form = RegisterForm()  # Если метод GET, то просто отображаем пустую форму для заполнения

    return render(request, 'accounts/register.html', {'form': form})  # Это путь к нашему шаблону HTML для отображения визуального вида нашей формы


def user_login(request):
    if request.method == 'POST':  # Проверяет заполнена ли форма да или нет
        form = LoginForm(request, data=request.POST)  # Если да, то заполняет нашу форму
        if form.is_valid():        # Проверяет валидацию, все ли прошло, все ли заполнено
            username = form.cleaned_data['username']  # Если все ок, то извлекает наши запоненые данные
            password = form.cleaned_data['password']  # Тут то же самое!
            user = authenticate(request, username=username, password=password) # Функция authenticate проверяет если такой пользователь, если да то возвращает его, если нет то возвращает None
            if user is not None:  # Если пользователь Не равен None
                login(request, user)  # То авторизует его
                return redirect('home')  # И отправляет его на главную страницу

    else:
        form = LoginForm()  # Если метод GET, то просто отображаем пустую форму для заполнения

    return render(request, 'accounts/login.html', {'form': form})  # Это путь к нашему шаблону HTML для отображения визуального вида нашей формы

def user_logout(request):
    logout(request)   # Разлогинивает пользователя
    return redirect('home')  # Направляет на главную страницу

# Обрабатывает форму профиля, чтоб его редактировать
@login_required  # Защита страници, чтоб только пользователь мог ее видеть
def profile(request):
    if request.method == 'POST':  # Отпрака заполнено формы
        user_form = UserUpdateForm(request.POST, instance=request.user)  # Проверяем заполнена ли она, параметр (instance) указывает связано ли это с текущим пользователем
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)  # То же самое
        if user_form.is_valid() and profile_form.is_valid():  # Если все ок
            user_form.save()  # То сохраняем все в модели User
            profile_form.save()  # Сохраняем в модели Profile
            return redirect('profile')  # Возвращает обратно в профиль
    else:
        user_form = UserUpdateForm(instance=request.user)  # Это в случаи если был метод GET, то выдает форму модели User
        profile_form = ProfileUpdateForm(instance=request.user.profile)  # Тут форму модели Profile

# В словарь передаются 3 формы
    bookings = Booking.objects.filter(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'bookings': bookings,
    }
    return render(request, 'accounts/profile.html', context)