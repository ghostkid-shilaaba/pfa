from django.db import models

class Salle(models.Model):
    ROOM_TYPES = (
        ('AMPHI', 'Amphithéâtre'),
        ('LABO', 'Laboratoire Informatique'),
        ('TD', 'Salle de cours'),
    )

    name = models.CharField(max_length=50, unique=True, verbose_name="Nom de la salle")
    capacity = models.PositiveIntegerField(verbose_name="Capacité")
    salle_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='TD')
    is_active = models.BooleanField(default=True, verbose_name="Disponible")
    description = models.TextField(blank=True, null=True, verbose_name="Description de la salle")
    has_projector = models.BooleanField(default=False, verbose_name="Projecteur")
    has_ac = models.BooleanField(default=False, verbose_name="Climatisation")

    def __str__(self):
        return f"{self.name} ({self.get_salle_type_display()})"