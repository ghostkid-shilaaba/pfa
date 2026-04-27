from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'role', 'telephone', 'matricule', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprime la contrainte d'unicité pour le web form
        if 'username' in self.fields:
            self.fields['username'].validators = []
            self.fields['username'].required = False # Permet de laisser vide si besoin