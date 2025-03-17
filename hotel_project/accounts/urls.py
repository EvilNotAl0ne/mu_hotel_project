from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'), # Маршрут для регистрации
]