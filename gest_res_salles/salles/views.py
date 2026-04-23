from django.shortcuts import render, get_object_or_404
from .models import Salle

def room_list(request):
    # On récupère toutes les salles actives
    rooms = Salle.objects.filter(is_active=True)
    return render(request, 'salles/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    # On récupère une salle spécifique par sa clé primaire (ID)
    room = get_object_or_404(Salle, pk=pk)
    return render(request, 'salles/room_detail.html', {'room': room})