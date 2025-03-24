from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'name', 'price_per_night', 'is_available')
    list_filter = ('room_number', 'name')
    search_fields = ('name',)

