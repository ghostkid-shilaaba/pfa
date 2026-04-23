from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('admin:index') # Redirige vers l'admin après le changement

    def form_valid(self, form):
        # C'est ici que ça se passe !
        response = super().form_valid(form)
        self.request.user.must_change_password = False
        self.request.user.save()
        return response
