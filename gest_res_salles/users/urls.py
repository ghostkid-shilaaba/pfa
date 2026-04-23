from django.urls import path, include
from .views import MyPasswordChangeView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
   
]