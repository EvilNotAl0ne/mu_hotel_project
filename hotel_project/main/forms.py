from django import forms
from .models import Booking

# Форма для поиска доступных комнат на основе дат заезда/выезда
class SearchForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата заезда"
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата выезда"
    )
    guests = forms.IntegerField(
        min_value=1,
        label="Количество гостей"
    )

# Форма для создания бронирования, которая включает дополнительные поля для контактной информации пользователя
class BookingForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Имя")
    last_name = forms.CharField(max_length=100, label="Фамилия")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, label="Номер телефона")

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'})
        }