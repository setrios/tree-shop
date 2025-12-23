from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.TreeListView.as_view(), name='tree-list'),
    path('trees/<int:pk>/', views.TreeDetailView.as_view(), name='tree-detail')
]
