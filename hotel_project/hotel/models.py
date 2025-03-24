from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name='Номер комнаты')
    name = models.CharField(max_length=100, default='Название номера', verbose_name='Название номера')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за комнату')
    capacity = models.PositiveIntegerField(verbose_name='Количество гостей')
    description = models.TextField(blank=True, verbose_name='Описание')
    amenities = models.CharField(max_length=250, blank=True, verbose_name='Удобства')
    is_available = models.BooleanField(default=True, verbose_name='Доступтность бронирования')
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name='Фотографии комнаты')

    def __str__(self):
        return f"{self.room_number} - {self.name}"