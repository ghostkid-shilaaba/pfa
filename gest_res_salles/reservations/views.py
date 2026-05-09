from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import time, datetime
from .models import Reservation
from .forms import ReservationForm
from salles.models import Salle


@login_required
def make_reservation(request, room_id):
    # 1. Sécurité Rôle
    if request.user.role == 'ETUDIANT':
        return HttpResponseForbidden("Les étudiants ne peuvent pas réserver.")

    room = get_object_or_404(Salle, pk=room_id)

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            # On crée l'objet sans le sauver en BDD pour faire nos checks
            res = form.save(commit=False)
            res.user = request.user
            res.room = room

            # --- VALIDATIONS MÉTIER ---
            
            # A. Pas le Dimanche (6 = Sunday)
            if res.date.weekday() == 6:
                messages.error(request, "Impossible de réserver le dimanche.")
                return render(request, 'reservations/booking_form.html', {'form': form, 'room': room})

            # B. Limites horaires (08:30 - 18:15)
            if res.start_time < time(8, 30) or res.end_time > time(18, 15):
                messages.error(request, "Les réservations doivent être entre 08:30 et 18:15.")
                return render(request, 'reservations/booking_form.html', {'form': form, 'room': room})

            # C. Cohérence des heures
            if res.start_time >= res.end_time:
                messages.error(request, "L'heure de fin doit être après le début.")
                return render(request, 'reservations/booking_form.html', {'form': form, 'room': room})

            # --- GESTION DES CONFLITS ---
            conflicts = Reservation.objects.filter(
                room=room,
                date=res.date,
                status='APPROVED'
            ).filter(
                Q(start_time__lt=res.end_time, end_time__gt=res.start_time)
            )

            if conflicts.exists():
                messages.error(request, "Cette salle est déjà occupée sur ce créneau.")
                return render(request, 'reservations/booking_form.html', {'form': form, 'room': room})

            # --- LOGIQUE DE STATUT ---
            if request.user.role == 'ADMIN' or request.user.is_superuser:
                res.status = 'APPROVED'
                messages.success(request, "Réservation validée directement !")
            else:
                res.status = 'PENDING'
                messages.info(request, "Demande envoyée, en attente de validation.")

            res.save()
            return redirect('rooms:room_list')
    else:
        # Cas GET : Formulaire vide
        form = ReservationForm()

    return render(request, 'reservations/booking_form.html', {'form': form, 'room': room})

# Ajoute ceci à la fin de reservations/views.py

@login_required
def admin_dashboard(request):
    # Vérification de sécurité pour que seuls les admins y accèdent
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return HttpResponseForbidden("Accès réservé à l'administration.")
    
    # On récupère toutes les réservations en attente (PENDING)
    pending_requests = Reservation.objects.filter(status='PENDING').order_by('date')
    
    return render(request, 'reservations/admin_dashboard.html', {
        'requests': pending_requests
    })

@login_required
def update_status(request, res_id, new_status):
    # Vérification de sécurité
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        reservation = get_object_or_404(Reservation, pk=res_id)
        
        # On met à jour le statut (APPROVED ou REJECTED)
        reservation.status = new_status
        reservation.save()
        statut = "approuvée" if new_status == 'APPROVED' else "refusée"
        messages.success(request, f"La demande de {reservation.user.username} a été {statut}.")
    else:
        return HttpResponseForbidden()
        
    return redirect('reservations:admin_dashboard')

@login_required
def my_reservations(request):
    # Un prof voit ses réservations, un admin voit tout
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        user_reservations = Reservation.objects.all().order_by('-date')
    else:
        user_reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'reservations/my_reservations.html', {'reservations': user_reservations})

@login_required 
def cancel_reservation(request, pk):
    # Sécurité : On vérifie que la réservation appartient bien à celui qui demande
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Réservation annulée avec succès.")
        return redirect('reservations:my_reservations')
    
    return render(request, 'reservations/confirm_cancel.html', {'reservation': reservation})

@login_required
def reservation_details(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Sécurité : Un prof ne peut voir que ses réservations, un admin peut voir tout
    if request.user.role != 'ADMIN' and not request.user.is_superuser and reservation.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas accès à cette réservation.")
    
    return render(request, 'reservations/reservation_details.html', {'reservation': reservation})

@login_required
def edit_reservation(request, pk):
    if request.user.role == 'ADMIN':
        res = get_object_or_404(Reservation, pk=pk)
    else:
        res = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == 'POST':
        new_date_str = request.POST.get('date')
        new_start_str = request.POST.get('start_time')
        new_end_str = request.POST.get('end_time')

        try:
            # 1. Conversion des chaînes de caractères en objets Python 'time' et 'date'
            # C'est cette étape qui règle ton erreur TypeError
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
            new_start = datetime.strptime(new_start_str, '%H:%M').time()
            new_end = datetime.strptime(new_end_str, '%H:%M').time()

            # 2. Check de l'ordre (Début avant Fin)
            if new_start >= new_end:
                messages.error(request, "L'heure de fin doit être après l'heure de début.")
                return render(request, 'reservations/edit_reservation.html', {'reservation': res})

            # 3. Check des bornes (08:30 - 18:15)
            # Maintenant que new_start est un objet time, la comparaison '<' fonctionne !
            if new_start < time(8, 30) or new_end > time(18, 15):
                messages.error(request, "Les horaires doivent être entre 08:30 et 18:15.")
                return render(request, 'reservations/edit_reservation.html', {'reservation': res})

            # 4. Check des conflits avec les autres
            conflicts = Reservation.objects.filter(
                room=res.room,
                date=new_date,
                status='APPROVED'
            ).exclude(pk=res.pk).filter(
                Q(start_time__lt=new_end, end_time__gt=new_start)
            )

            if conflicts.exists():
                messages.error(request, "Ce créneau est déjà réservé par un autre professeur.")
                return render(request, 'reservations/edit_reservation.html', {'reservation': res})

            # --- SAUVEGARDE ---
            res.date = new_date
            res.start_time = new_start
            res.end_time = new_end
            
            if request.user.role != 'ADMIN':
                res.status = 'PENDING'
                messages.info(request, "Modifié ! Votre demande est repassée en attente de validation.")
            else:
                messages.success(request, "Réservation mise à jour.")

            res.save()
            return redirect('reservations:my_reservations')

        except ValueError:
            messages.error(request, "Format de date ou d'heure invalide.")
            return render(request, 'reservations/edit_reservation.html', {'reservation': res})

    return render(request, 'reservations/edit_reservation.html', {'reservation': res})