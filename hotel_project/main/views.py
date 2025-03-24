from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotel.models import Room
from .models import Booking
from .forms import SearchForm, BookingForm
from .utils import send_cancel_email
from datetime import date

# Главная страница, позволяет пользователю искать доступные комнаты
def home(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        guests = form.cleaned_data['guests']
        return redirect('search_results', check_in=check_in.isoformat(), check_out=check_out.isoformat(), guests=guests)
    return render(request, 'main/home.html', {'form': form})

# Отображает список доступных комнат
def search_results(request, check_in, check_out, guests):
    # Преобразуем строки обратно в объекты date
    check_in_date = date.fromisoformat(check_in)
    check_out_date = date.fromisoformat(check_out)
    guests = int(guests)

    # Получаем доступные комнаты
    available_rooms = Booking.get_available_rooms(check_in_date, check_out_date).filter(capacity__gte=guests)

    return render(request, 'main/search_results.html', {
        'available_rooms': available_rooms,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests
    })

# Позволяет пользователю забронировать выбранную комнату
def book_room(request, room_id, check_in, check_out, guests):
    room = get_object_or_404(Room, id=room_id)
    check_in_date = date.fromisoformat(check_in)
    check_out_date = date.fromisoformat(check_out)

    # Проверка доступна ли комната
    if not Booking.is_room_available(room, check_in_date, check_out_date):
        messages.error(request, 'Комната не доступна на выбранные даты.')
        return redirect('search_results', check_in=check_in, check_out=check_out, guests=guests)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user if request.user.is_authenticated else None
            booking.save()

            booking.first_name = form.cleaned_data['first_name']
            booking.last_name = form.cleaned_data['last_name']
            booking.email = form.cleaned_data['email']
            booking.phone = form.cleaned_data['phone']
            booking.save()

            send_cancel_email(booking)

            messages.success(request, 'Бронирование успешно создано. Проверти вашу почту!')
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        # Заполняем форму начальными данными
        initial_data = {
            'check_in': check_in_date,
            'check_out': check_out_date,
            'guests': guests,
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'main/book_room.html', {'form': form, 'room': room})

@login_required
def cancel_booking(request, booking_id):
    # Получаем бронирование по ID
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    # Удаляем бронирование
    booking.delete()
    messages.success(request, "Бронирование успешно отменено.")
    return redirect('profile')

def cancel_booking_by_token(request, token):
    print(f"Received token from URL: {token}")  # Отладочный вывод (будет приходить токен в терминал из URL)
    booking = get_object_or_404(Booking, cancel_token=token)
    booking.delete()  # Удаляем бронирование
    messages.success(request, "Бронирование успешно отменено.")
    return redirect('home')  # Перенаправляем на главную страницу