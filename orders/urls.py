from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.add_address, name='add_address'),
    path('delete-address/<int:pk>', views.delete_address, name='delete_address'),
    path('update-address/<int:pk>', views.update_address, name='update_address'),
    path('place-order/', views.place_order, name='place_order'),
    
]
