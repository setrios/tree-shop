from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Tree, Color, Decoration, Type
from .forms import TreeFilterForm

# Create your views here.

class TreeListView(ListView):
    model = Tree

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = TreeFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data

            if data['colors']:
                queryset = queryset.filter(color__in=data['colors'])

            if data['decorations']:
                queryset = queryset.filter(decorations__in=data['decorations'])

            if data['tree_types']:
                queryset = queryset.filter(tree_type__in=data['tree_types'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class TreeDetailView(DetailView):
    model = Tree