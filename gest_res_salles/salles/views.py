import io  
import csv
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Salle
from .forms import SalleForm

def room_list(request):
    # On récupère toutes les salles actives
    rooms = Salle.objects.filter(is_active=True)
    return render(request, 'salles/room_list.html', {'rooms': rooms})

# Dans salles/views.py
def room_detail(request, pk):
    room = get_object_or_404(Salle, pk=pk)
    # Récupère les réservations approuvées à partir d'aujourd'hui
    occupations = room.reservation_set.filter(status='APPROVED', date__gte=date.today()).order_by('date', 'start_time')
    return render(request, 'salles/room_detail.html', {'room': room, 'occupations': occupations})

@login_required
def add_room(request):
    """Vue pour ajouter une salle manuellement via le formulaire"""
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return HttpResponseForbidden("Accès réservé aux administrateurs.")

    if request.method == "POST":
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"La salle {form.cleaned_data['name']} a été créée.")
            return redirect('rooms:room_list')
    else:
        form = SalleForm()
    
    return render(request, 'salles/add_room.html', {'form': form})

@login_required
def import_rooms_csv(request):
    """Vue pour l'importation massive de salles via un fichier CSV"""
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=';')
            next(reader)  # Sauter l'en-tête (Nom;Capacité;Type)

            count = 0
            for row in reader:
                # row[0]=nom, row[1]=capacité, row[2]=type
                Salle.objects.get_or_create(
                    name=row[0],
                    capacity=int(row[1]),
                    salle_type=row[2]
                )
                count += 1
            
            messages.success(request, f"{count} salles ont été importées avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'importation : {e}")
            
        return redirect('rooms:room_list')

    return render(request, 'salles/import_rooms.html')