from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number',
            'price_per_night',
            'capacity',
            'description',
            'amenities',
            'is_available',
            'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

