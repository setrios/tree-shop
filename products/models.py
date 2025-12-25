from django.db import models

# Create your models here.

class Tree(models.Model):
    image = models.ImageField(upload_to='trees/')
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    artificial = models.BooleanField()
    tree_type = models.ForeignKey('Type', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    decorations = models.ManyToManyField('Decoration', blank=True)  # null=True unacceptable as separete table
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} | {self.height}'
    

class Type(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Decoration(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

