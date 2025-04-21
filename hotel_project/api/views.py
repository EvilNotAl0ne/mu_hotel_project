from rest_framework.views import APIView
from rest_framework.response import Response
from hotel.models import Room, RoomCategory
from main.models import Booking
from .serializers import RoomSerializer, BookingSerializer, RoomCategorySerializer


class RoomAPI(APIView):
    """
    API для работы с комнатами.
    Поддерживает GET-запросы для получения списка доступных комнат
    и POST-запросы для создания новой комнаты.
    """

    def get(self, request):
        """
        Получает список доступных комнат с учетом фильтров:
        - category_id: ID категории комнаты (опционально).
        - check_in и check_out: даты заезда и выезда (опционально).
        """
        # Извлекаем параметры из запроса
        category_id = request.query_params.get("category")
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")

        # Фильтруем комнаты по категории и датам
        rooms = Room.objects.all()
        if category_id:
            rooms = rooms.filter(category_id=category_id)
        if check_in and check_out:
            rooms = rooms.exclude(
                bookings__check_in__lt=check_out,
                bookings__check_out__gt=check_in
            )

        # Сериализуем результат
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Создает новую комнату на основе данных из запроса.
        """
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookingListAPI(APIView):
    """
    API для работы со списком бронирований.
    Поддерживает GET-запросы для получения списка бронирований
    и POST-запросы для создания нового бронирования.
    """

    def get(self, request):
        """
        Получает список бронирований.
        Можно фильтровать по email пользователя.
        """
        email = request.query_params.get("email")
        if email:
            bookings = Booking.objects.filter(email=email)
        else:
            bookings = Booking.objects.all()

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Создает новое бронирование на основе данных из запроса.
        """
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print("Validation errors:", serializer.errors)  # Отладочный вывод
        return Response(serializer.errors, status=400)


class BookingDetailAPI(APIView):
    """
    API для работы с конкретным бронированием.
    Поддерживает GET-запросы для получения информации о бронировании
    и DELETE-запросы для удаления бронирования.
    """

    def get(self, request, pk):
        """
        Получает информацию о бронировании по его ID.
        """
        try:
            booking = Booking.objects.get(pk=pk)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({"detail": "Бронирование не найдено."}, status=404)

    def delete(self, request, pk):
        """
        Удаляет бронирование по его ID.
        """
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
            return Response(status=204)  # Успешное удаление без содержимого
        except Booking.DoesNotExist:
            return Response({"detail": "Бронирование не найдено."}, status=404)


class RoomCategoryAPI(APIView):
    """
    API для работы с категориями комнат.
    Поддерживает GET-запросы для получения списка категорий.
    """

    def get(self, request):
        """
        Получает список всех категорий комнат.
        """
        categories = RoomCategory.objects.all()
        print("Categories:", categories)  # Отладочный вывод
        serializer = RoomCategorySerializer(categories, many=True)
        return Response(serializer.data)
