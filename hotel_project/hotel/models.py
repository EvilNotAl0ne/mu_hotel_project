from django.db import models

class RoomCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание категории')


    def __str__(self):
        return self.name

class CategoryImage(models.Model):
    category = models.ForeignKey(
        RoomCategory,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    image = models.ImageField(upload_to='category_images/', verbose_name='Изображение')

    def __str__(self):
        return f"Изображение для {self.category.name}"


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name='Номер комнаты')
    name = models.CharField(max_length=100, default='Название номера', verbose_name='Название номера')
    category = models.ForeignKey(
        RoomCategory,
        related_name='rooms',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за комнату')
    capacity = models.PositiveIntegerField(verbose_name='Количество гостей')
    description = models.TextField(blank=True, verbose_name='Описание')
    amenities = models.CharField(max_length=250, blank=True, verbose_name='Удобства')
    is_available = models.BooleanField(default=True, verbose_name='Доступность бронирования')

    def __str__(self):
        return f"{self.room_number} - {self.name}"

def room_image_upload_path(instance, filename):
    # Создаем путь для загрузки изображений: rooms/<room_name>/<filename>
    return f"rooms/{instance.room.name}/{filename}"

class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Комната'
    )
    image = models.ImageField(upload_to='room_images/', verbose_name='Изображение')

    def __str__(self):
        return f"Изображение для {self.room.name}"