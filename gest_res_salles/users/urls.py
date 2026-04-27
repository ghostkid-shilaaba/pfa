from django.urls import path, include

from . import views, models
from .views import MyPasswordChangeView



urlpatterns = [
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('', include('django.contrib.auth.urls')),
    path('list/', views.user_list, name='user_list'), # Pour voir les utilisateurs
    path('import/', views.import_users, name='import_users'),
   
]