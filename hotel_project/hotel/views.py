from django.shortcuts import render, get_object_or_404
from .models import RoomCategory, Room
from datetime import datetime, timedelta
from main.models import Booking


# Функция просмотра комнат (доступ есть у всех)
def room_list(request):
    categories = RoomCategory.objects.all()
    return render(request, 'hotel/room_list.html', {'categories': categories})

def book_room(request, room_id, check_in, check_out, guests):
    # Получаем комнату по ID
    room = get_object_or_404(Room, pk=room_id)

    # Передаем данные в шаблон
    return render(request, 'hotel/book_room.html', {
        'room': room,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
    })

def category_detail(request, pk):
    category = get_object_or_404(RoomCategory, pk=pk)

    today = datetime.today().date()

    # Устанавливаем значения по умолчанию
    check_in = request.GET.get('check_in', today)
    check_out = request.GET.get('check_out', today + timedelta(days=1))  # Завтрашняя дата
    guests = int(request.GET.get('guests', 1))  # По умолчанию 1 гость

    # Преобразуем строки в объекты datetime.date
    try:
        # Проверяем, является ли check_in строкой перед преобразованием
        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        else:
            check_in = today  # Если check_in уже является датой, используем его

        # Проверяем, является ли check_out строкой перед преобразованием
        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
        else:
            check_out = today + timedelta(days=1)  # Если check_out уже является датой, используем его

    except ValueError:
        # Если формат даты неверный, используем значения по умолчанию
        check_in = today
        check_out = today + timedelta(days=1)

    # Фильтруем комнаты по категории и вместимости
    rooms = category.rooms.filter(is_available=True, capacity__gte=int(guests))

    # Исключаем забронированные комнаты
    booked_rooms = Booking.objects.filter(
        check_in__lt=check_out,
        check_out__gt=check_in
    ).values_list('room_id', flat=True)
    available_rooms = rooms.exclude(id__in=booked_rooms)

    return render(request, 'hotel/category_detail.html', {
        'category': category,
        'rooms': available_rooms,  # Передаем только доступные комнаты
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
    })


