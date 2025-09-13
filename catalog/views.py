from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    """Контроллер для отображения домашней страницы"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    """Контроллер для отображения детальной информации о товаре"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
