from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('ajouter/', views.add_room, name='add_room'),
    path('import-csv/', views.import_rooms_csv, name='import_csv'),
]