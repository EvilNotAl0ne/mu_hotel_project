from django import forms
from .models import Room, RoomImage

class RoomForm(forms.ModelForm):
    # Поле для загрузки нескольких изображений
    images = forms.FileField(
        widget=forms.FileInput(),  # Убираем атрибут multiple=True
        required=False,
        label="Фотографии комнаты"
    )

    class Meta:
        model = Room
        fields = [
            'room_number',
            'price_per_night',
            'capacity',
            'description',
            'amenities',
            'is_available',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        # Сначала сохраняем комнату
        room = super().save(commit=commit)

        # Получаем список загруженных файлов
        if self.files and 'images' in self.files:
            for image in self.files.getlist('images'):  # Обрабатываем все файлы
                # Создаем запись в модели RoomImage для каждого файла
                RoomImage.objects.create(room=room, image=image)

        return room
