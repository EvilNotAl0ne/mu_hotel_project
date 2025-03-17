from django import forms

class RoomSearchForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата заезда')
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата выезда')