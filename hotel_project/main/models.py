from django.db import models
from django.contrib.auth.models import User  # Импортируется встроенная модель User из Django
from hotel.models import Room
import uuid  # Это модуль генерирует токен

class Booking(models.Model):  # Эта модель будет представлять бронирование комнаты
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()  # Хранит дату заезда
    check_out = models.DateField()  # Хранит дату выезда
    guests = models.IntegerField()  # Хранит количество гостей
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)  # Это внешний ключ, который связывает бронирование с моделью User
    cancel_token = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)  # Хранит уникальный токен для отмены бронирования
    #  Хранить дополнительную информацию о госте
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.room.name} ({self.check_in} - {self.check_out})"

    # Проверяет доступна ли комната на указанные даты
    @staticmethod
    def is_room_available(room, check_in, check_out):
        return not Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

    # Возвращает список доступных комнат на указанные даты
    @staticmethod
    def get_available_rooms(check_in, check_out):
        booked_rooms = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        return Room.objects.exclude(id__in=booked_rooms)

