from django import forms
from .models import Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('p_name', 's_name', 'address', 'zip_numero', 'city')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price_max', 'price', 'image')