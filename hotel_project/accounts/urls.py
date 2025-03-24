from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), # Путь для регистрации
    path('login/', views.user_login, name='login'),  #  Путь для входа
    path('logout/', views.user_logout, name='logout'),  # Путь для выхода
    path('profile/', views.profile, name='profile'),  # Путь до профиля пользователя
]