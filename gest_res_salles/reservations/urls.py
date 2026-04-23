
from django.urls import path
from . import views

app_name = 'reservations'  

urlpatterns = [
    # Si tu n'as pas encore créé la vue, crée une fonction vide dans views.py
    path('book/<int:room_id>/', views.make_reservation, name='book_room'),
]