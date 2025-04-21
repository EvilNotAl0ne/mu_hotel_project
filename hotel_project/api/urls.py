from django.urls import path
from .views import RoomAPI, BookingListAPI, BookingDetailAPI, RoomCategoryAPI

urlpatterns = [
    path('api/rooms/', RoomAPI.as_view(), name='room_api'),  # API для работы с комнатами
    path('api/room-categories/', RoomCategoryAPI.as_view(), name='room_category_api'),  # API для работы с категориями комнат
    path('api/bookings/', BookingListAPI.as_view(), name='booking_list_api'),  # API для работы со списком бронирований
    path('api/bookings/<int:pk>/', BookingDetailAPI.as_view(), name='booking_detail_api'),  # API для работы с конкретным бронированием (по ID)
]