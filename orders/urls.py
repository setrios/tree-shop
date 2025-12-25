from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.add_address, name='add_address'),
]
