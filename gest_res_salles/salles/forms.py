from django import forms
from .models import Salle

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        # On inclut les champs importants pour la création
        fields = ['name', 'capacity', 'salle_type', 'is_active', 'has_projector', 'has_ac', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ex: Salle 101 ou Amphi A'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1'
            }),
            'salle_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Matériel disponible, localisation...'
            }),
            # Les BooleanField (checkbox) se gèrent avec form-check-input
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_projector': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }