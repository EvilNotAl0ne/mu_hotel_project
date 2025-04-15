from django.contrib import admin
from .models import RoomCategory, Room, CategoryImage, RoomImage


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 4  # Количество пустых полей для добавления новых изображений

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 4  # Количество пустых полей для добавления новых изображений

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CategoryImageInline]  # Добавляем возможность загрузки нескольких изображений

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'name', 'category', 'price_per_night', 'capacity', 'is_available')
    list_filter = ('room_number', 'name')
    search_fields = ('name',)
    inlines = [RoomImageInline]  # Добавляем возможность загрузки нескольких изображений для комнат
