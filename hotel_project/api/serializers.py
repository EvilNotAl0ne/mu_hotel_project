from rest_framework import serializers
from hotel.models import Room, RoomCategory
from main.models import Booking

# Сериализатор для категорий комнат
class RoomCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RoomCategory.
    Включает поля: ID, название, описание и удобства.
    """
    amenities = serializers.SerializerMethodField()

    class Meta:
        model = RoomCategory
        fields = ['id', 'name', 'description', 'amenities']

    def get_amenities(self, obj):
        """
        Получает список удобств из первой комнаты данной категории.
        Если удобства отсутствуют, возвращает пустой список.
        """
        first_room = obj.rooms.first()
        if first_room and first_room.amenities:
            return first_room.amenities.split(",")
        return []

    def get_images(self, obj):
        """
        Получает список URL-адресов изображений для данной категории.
        """
        return [image.image.url for image in obj.images.all()]

# Сериализатор для комнат
class RoomSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Room.
    Включает поля: ID, название, описание и цена за ночь.
    """
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'price_per_night']

# Сериализатор для бронирований
class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Booking.
    Включает все поля модели.
    """
    class Meta:
        model = Booking
        fields = '__all__'