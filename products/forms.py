from django import forms
from .models import Color, Decoration, Type

class TreeFilterForm(forms.Form):
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    decorations = forms.ModelMultipleChoiceField(
        queryset=Decoration.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    tree_types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
