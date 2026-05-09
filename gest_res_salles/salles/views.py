import io  
import csv
from datetime import date,datetime, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Salle
from .forms import SalleForm
from reservations.models import Reservation
from django.db.models import Q

def room_list(request):
    # On commence avec toutes les salles actives
    salles = Salle.objects.filter(is_active=True)

    # --- FILTRES TEXTE ET CHOIX ---
    query = request.GET.get('q')
    if query:
        salles = salles.filter(name__icontains=query)

    salle_type = request.GET.get('type')
    if salle_type:
        salles = salles.filter(salle_type=salle_type)

    capacity_min = request.GET.get('capacity_min')
    if capacity_min:
        salles = salles.filter(capacity__gte=capacity_min)

    # --- FILTRES ÉQUIPEMENTS (Checkboxes) ---
    if request.GET.get('has_projector'):
        salles = salles.filter(has_projector=True)
    
    if request.GET.get('has_ac'):
        salles = salles.filter(has_ac=True)

    # --- FILTRE DE DISPONIBILITÉ (Le cerveau du système) ---
    date_query = request.GET.get('date')
    start_query = request.GET.get('start_time')
    end_query = request.GET.get('end_time')

    if date_query and start_query and end_query:
        try:
            # On identifie les salles déjà réservées (APPROVED) sur ce créneau
            occupied_rooms = Reservation.objects.filter(
                date=date_query,
                status='APPROVED'
            ).filter(
                Q(start_time__lt=end_query, end_time__gt=start_query)
            ).values_list('room_id', flat=True)

            # On exclut ces salles de la liste finale
            salles = salles.exclude(id__in=occupied_rooms)
        except ValueError:
            pass # Gestion d'erreur si format heure invalide

    context = {
        'salles': salles,
        'room_types': Salle.ROOM_TYPES,
    }
    return render(request, 'salles/room_list.html', context)

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
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            # Utiliser DictReader est plus propre quand on a beaucoup de colonnes
            reader = csv.DictReader(io_string, delimiter=';')

            count = 0
            for row in reader:
                # On nettoie et on convertit les données
                # .get('Nom') doit correspondre exactement à l'en-tête de ton CSV
                salle_nom = row.get('Nom')
                if not salle_nom: continue # Saute les lignes vides

                # Logique pour transformer "1" ou "True" en Boolean Django
                def to_bool(val):
                    return str(val).lower() in ['1', 'true', 'oui', 'yes']

                Salle.objects.update_or_create(
                    name=salle_nom,
                    defaults={
                        'capacity': int(row.get('Capacité', 0)),
                        'salle_type': row.get('Type', 'TD'),
                        'has_projector': to_bool(row.get('Projecteur', False)),
                        'has_ac': to_bool(row.get('Climatisation', False)),
                        'description': row.get('Description', ''),
                        'is_active': True
                    }
                )
                count += 1
            
            messages.success(request, f"{count} salles ont été traitées (ajoutées ou mises à jour).")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'importation : {e}")
            
        return redirect('rooms:room_list')

    return render(request, 'salles/import_rooms.html')