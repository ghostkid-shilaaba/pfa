from django.shortcuts import render,redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
import csv, io
from django.contrib.auth.decorators import login_required

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('rooms:room_list')

    def form_valid(self, form):
        user = form.save() 
        user.must_change_password = False
        user.save()
        return super().form_valid(form)

@login_required
def import_users(request):
    # Sécurité Admin
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        return redirect('home')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            # On décode le fichier
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            # DictReader utilise la première ligne comme clés
            reader = csv.DictReader(io_string, delimiter=';') 

            count = 0
            errors = 0

            for row in reader:
                email = row.get('email')
                if not email:
                    continue
                
                # On vérifie si l'utilisateur existe déjà
                if not User.objects.filter(email=email).exists():
                    try:
                        # create_user gère automatiquement le hashage du mot de passe
                        user = User.objects.create_user(
                            email=email,
                            username=row.get('username', email.split('@')[0]), # Fallback sur l'email si pas de nom
                            role=row.get('role', 'ETUDIANT'),
                            telephone=row.get('telephone', ''),
                            matricule=row.get('matricule', ''),
                            password=row.get('password', 'Pass12345'),
                            must_change_password=True # Optionnel : force le changement au 1er login
                        )
                        count += 1
                    except Exception:
                        errors += 1
                else:
                    # Optionnel : Mettre à jour les infos si l'user existe déjà
                    user = User.objects.get(email=email)
                    user.telephone = row.get('telephone', user.telephone)
                    user.matricule = row.get('matricule', user.matricule)
                    user.save()

            messages.success(request, f"{count} utilisateurs importés. ({errors} erreurs)")
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier : {e}")
            
        return redirect('user_list') # Redirige vers ta liste d'utilisateurs maison

    return render(request, 'users/import.html')

@login_required
def user_list(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'users/user_list.html', {'users': users})