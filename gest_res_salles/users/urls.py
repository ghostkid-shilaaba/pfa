from django.urls import path, include
from .views import MyPasswordChangeView

urlpatterns = [
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('', include('django.contrib.auth.urls')),
    
   
]