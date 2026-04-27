from django.shortcuts import render,redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
import csv, io

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('rooms:room_list')

    def form_valid(self, form):
        user = form.save() 
        user.must_change_password = False
        user.save()
        return super().form_valid(form)

def import_users(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        count = 0
        for row in reader:
            email = row.get('email')
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    username=row.get('username', ''),
                    role=row.get('role', 'ETUDIANT'),
                    telephone=row.get('telephone', ''),
                    matricule=row.get('matricule', ''),
                    password=row.get('password', 'Pass12345') 
                )
                count += 1
        
        messages.success(request, f"{count} utilisateurs importés avec succès.")
        return redirect('admin:users_user_changelist')
        
    return render(request, 'users/import.html')

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})