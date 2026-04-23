from django.db import models
from django.conf import settings
from salles.models import Salle

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Refusée'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    purpose = models.CharField(max_length=200, help_text="Ex: Cours de Réseaux, Réunion...")

    def __str__(self):
        return f"{self.user.username} - {self.room.name} ({self.date})"