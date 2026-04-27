from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('book/<int:room_id>/', views.make_reservation, name='make_reservation'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update/<int:res_id>/<str:new_status>/', views.update_status, name='update_status'),
    path('mes-reservations/', views.my_reservations, name='my_reservations'),
    
]