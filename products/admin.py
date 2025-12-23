from django.contrib import admin
from .models import Tree, Type, Color, Decoration

# Register your models here.

admin.site.register(Tree)
admin.site.register(Type)
admin.site.register(Color)
admin.site.register(Decoration)