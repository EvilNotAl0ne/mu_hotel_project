from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'), # Маршрут для всех категорий
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('book/<int:room_id>/<str:check_in>/<str:check_out>/<int:guests>/', views.book_room, name='book_room'),
]