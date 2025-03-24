from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from hotel.models import Room
from main.models import Booking
from .forms import RoomForm
from datetime import date, timedelta

# Функция проверяет пользователь админ или обычный
def is_admin(user):
    return user.is_staff  # Если да, то дает доступ только админам

# Функция просмотра комнат (доступ есть у всех)
@login_required
def room_list(request):
    # Получаем текущие даты (например, сегодняшнюю дату и +7 дней)
    today = date.today()
    future_date = today + timedelta(days=100)

    # Получаем доступные комнаты
    available_rooms = Booking.get_available_rooms(today, future_date)

    return render(request, 'hotel/room_list.html', {'rooms': available_rooms})

# Функция добавления комнат(доступ только админ)
@user_passes_test(is_admin)
def add_room(request):
    if request.method == 'POST':  #  Если метод POST значит пользователь оправил заполненную форму
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():  # Если форма валидна
            form.save()  # То сохраняем в БД
            return redirect('room_list')  # Отправляем обратно к списку
    else:
        form = RoomForm()  # Если запрос GET отправляем пустую форму
    return render(request, 'hotel/add_room.html', {'form': form})

# Функция редактирования комнат(доступ только админ)
@user_passes_test(is_admin)
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)  # Проверка существует это комната или нет
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)  # instance связь с текущей комнатой
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return  render(request, 'hotel/edit_room.html', {'form': form})

# Функция удаления комнат(доступ только админ)
@user_passes_test(is_admin)
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'hotel/delete_room.html', {'room': room})
