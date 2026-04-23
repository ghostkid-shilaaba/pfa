from django.contrib import admin
from .models import Salle

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
  
    list_display = ('name', 'salle_type', 'capacity', 'is_active', 'has_projector')
    
   
    search_fields = ('name',)
    
   
    list_filter = ('salle_type', 'is_active', 'has_projector', 'has_ac')
    
   
    fieldsets = (
        (None, {
            'fields': ('name', 'salle_type', 'capacity')
        }),
        ('Équipements & Statut', {
            'fields': ('is_active', 'has_projector', 'has_ac', 'description'),
            'classes': ('collapse',), 
        }),
    )
