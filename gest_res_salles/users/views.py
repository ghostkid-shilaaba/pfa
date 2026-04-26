from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('rooms:room_list')

    def form_valid(self, form):
        user = form.save() 
        user.must_change_password = False
        user.save()
        return super().form_valid(form)
