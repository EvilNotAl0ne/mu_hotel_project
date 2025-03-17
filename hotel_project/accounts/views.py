from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':  # Провереям был ли POST запрос
        form = RegisterForm(request.POST)
        if form.is_valid():  # Провереям была ли коректно заполнина наша форма
            user = form.save()  # Если все ок, то сохроняем
            login(request, user)  # Если так же все ок, то авторизуем пользователя
            return redirect('home') # И перемещаем его на главную строницу

    else:
        form = RegisterForm() # Если метод GET то просто отоброжаем пустую форму для заполнения

    return render(request, 'accounts/register.html', {'form': form})  # Это путь к нашему шаблону HTML для отображения визуального вида нашей формы


