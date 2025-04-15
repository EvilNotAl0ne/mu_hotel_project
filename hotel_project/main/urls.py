from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # Маршрут для страницы "Об отеле"
    path('search/<str:check_in>/<str:check_out>/<int:guests>/', views.search_results, name='search_results'),  # Маршрут для пояска комнат
    path('book/<int:room_id>/<str:check_in>/<str:check_out>/<int:guests>/', views.book_room, name='book_room'),  # Маршрут для бронирования комнаты
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # Маршрут для отмены бронирования по ID
    path('cancel/<str:token>/', views.cancel_booking_by_token, name='cancel_booking_by_token'),  # Маршрут для отмены бронирования по токену
]