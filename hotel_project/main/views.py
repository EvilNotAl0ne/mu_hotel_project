from django.shortcuts import render
from hotel.models import Room
from .forms import RoomSearchForm

def home(request):
    form = RoomSearchForm(request.GET or None)
    rooms = Room.objects.filter(is_available=True)

    if form.is_valid():
        check_in_date = form.cleaned_data['check_in_date']
        check_out_date = form.cleaned_data['check_out_date']


        rooms = rooms.filter(is_available=True)

    return render(request, 'main/home.html', {'form': form, 'rooms': rooms})
