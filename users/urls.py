from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # register is not in django.contrib.auth.urls
    path('', include('django.contrib.auth.urls'))  # to use prebuild login/logout/... urls 
]
