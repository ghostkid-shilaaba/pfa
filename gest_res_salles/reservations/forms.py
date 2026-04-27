from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'min': '08:30', 'max': '18:15'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'min': '08:30', 'max': '18:15'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: TP Réseaux'}),
        }

