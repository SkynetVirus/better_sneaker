from django.shortcuts import render
from django.http import HttpResponse
from .models import (Product,Color,Size,Brand)
from category.models import (Category)
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    return render(request, 'templates/shop.html', {
        'products': products,
        'categories' : categories,
        'colors' : colors,
        'sizes' : sizes,
        'brands' : brands
    })


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'templates/product.html', {'instance': product})
