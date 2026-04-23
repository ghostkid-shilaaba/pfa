# reservations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Reservation
from salles.models import Salle # Vérifie si ton modèle s'appelle Salle ou Room

@login_required
def make_reservation(request, room_id):
    # 1. Sécurité : Bloquer les étudiants
    if request.user.role == 'ETUDIANT':
        return HttpResponseForbidden("Vous n'avez pas les droits pour réserver une salle.")

    # 2. Récupérer la salle (pour l'afficher dans le formulaire)
    room = get_object_or_404(Salle, pk=room_id)

    # 3. TRAITEMENT DU FORMULAIRE (POST)
    if request.method == "POST":
        reservation = Reservation(
            user=request.user,
            room_id=room_id,
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            purpose=request.POST.get('purpose')
        )

        # Logique de pouvoir
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            reservation.status = 'APPROVED'
        else:
            reservation.status = 'PENDING'

        reservation.save()
        return redirect('rooms:room_list')

    # 4. AFFICHAGE DU FORMULAIRE (GET)
    # Si ce n'est pas un POST, on renvoie le template HTML
    return render(request, 'reservations/booking_form.html', {'room': room})