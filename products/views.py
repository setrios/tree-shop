from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Tree

# Create your views here.

class TreeListView(ListView):
    model = Tree


class TreeDetailView(DetailView):
    model = Tree