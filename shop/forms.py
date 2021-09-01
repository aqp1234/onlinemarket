from django import forms
from .models import Category, Product
from django.core.validators import MinValueValidator

class ProductForm(forms.Form):
    categories = Category.objects.all()
    choices = []
    for category in categories:
        choices.append((category.id, category.name))
    category = forms.ChoiceField(label="카테고리", choices=tuple(choices))
    name = forms.CharField(max_length=200)
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)
    meta_description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()
    stock = forms.IntegerField(validators=[MinValueValidator(0)])
    available_display = forms.BooleanField()
    available_order = forms.BooleanField()
    