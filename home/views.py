from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from .context_processors import home_config
from product.models import (Product,Brand)
from category.models import (Category)
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    context = {}
    config = home_config(request)['home_config']
    brands = Brand.objects.all()
    context['brands'] = brands
    if config.show_banner_1:
        context['banner_1'] = config.banner_product
    if config.show_characteristics:
        pass
    if config.show_deals_featured:
        deals_of_weeds = Product.objects.filter(sale__gt=0,rated__gt=0).order_by('-sale','-rated')[:3]
        featured_items = Product.objects.order_by('-view_counter')[:8]
        on_sale_items = Product.objects.filter(sale__gt=0).order_by('-sale')[:8]
        best_rated_items = Product.objects.filter(rated__gt=0).order_by('-rated')[:8]
        context['deals_featured'] = {
            'weed' : deals_of_weeds,
            'featured' : featured_items,
            'on_sale' : on_sale_items,
            'best_rated' : best_rated_items
        }

    if config.show_popular_categories:
        popular_categories = Category.objects.all()
        context['popular_categories'] = popular_categories
    if config.show_banner_2:
        banner_2 = Product.objects.all()[:3]
        context['banner_2'] = banner_2
    if config.show_new_arrivals:
        pass
    if config.show_best_sellers:
        best_sellers = Product.objects.filter(sale__gt=0).order_by('-sale')
        sellers_statistical = best_sellers.values('category').order_by(
            'category__name').annotate(count=Count('category'))
        categories = []
        for cate in sellers_statistical:
            category_obj = get_object_or_404(Category,pk=cate['category'])
            list_product_with_category = best_sellers.filter(category__pk=category_obj.pk)
            categories.append({
                'name' : category_obj.name,
                'items': list_product_with_category
            })
        context['best_sellers'] = {
            'top20': best_sellers[:20],
            'categories': categories
        }
    if config.show_trends:
        pass
    if config.show_latest_reviews:
        pass
    if config.show_viewed:
        pass
    return render(request, 'templates/index.html', context=context)

def contact(request):
    return render(request,'templates/contact.html')
