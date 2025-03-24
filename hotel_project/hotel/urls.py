from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'), # Маршрут всех доступных комнат
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:pk>', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:pk>', views.delete_room, name='delete_room'),
]