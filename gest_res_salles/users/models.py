from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ETUDIANT', 'Étudiant'),
        ('ENSEIGNANT', 'Enseignant'),
        ('ADMIN', 'Administrateur'),
    )
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='ETUDIANT')
    telephone = models.CharField(max_length=15, blank=True, null=True)
    matricule = models.CharField(max_length=50, unique=True, blank=True, null=True)
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"