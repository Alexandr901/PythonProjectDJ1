from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Product

class HomeView(ListView):
    """CBV для отображения домашней страницы"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    """CBV для отображения детальной информации о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    """CBV для отображения страницы контактов"""
    template_name = 'catalog/contacts.html'
