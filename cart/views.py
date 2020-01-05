from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse as jsonRes
from .models import (Cart, CartItem)
from product.models import (Product, Size, Color)

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('home:index') + '#login')
    cart = Cart.objects.filter(user=request.user, complete=False).first()
    return render(request, 'templates/cart.html', {'instance': cart})

def remove_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id', None)
        if not cart_item_id:
            return jsonRes({
                'data': 'error',
                'msg': 'cart_item_id required!'
            })
        cart_item = CartItem.objects.filter(id=cart_item_id).first()
        if not cart_item:
            return jsonRes({
                'data': 'error',
                'msg': 'cart item not found!'
            })
        cart_empty = True if cart_item.cart.items.count() == 1 else False
        result_deleted = cart_item.delete()
        return jsonRes({
            'data': 'success',
            'object_deleted': result_deleted[1],
            'cart_empty' : cart_empty
        })

    return jsonRes({
        'data': 'error',
        'msg': 'Accept denied!'
    })


def add_item(request):
    if not request.user.is_authenticated:
        return jsonRes({
            'data': 'error',
            'target': 'login',
            'msg': 'You need to login!'
        })
    if request.method == 'POST':
        product_id = request.POST.get('product_id', None)
        size_id = request.POST.get('size_id', None)
        color_id = request.POST.get('color_id', None)
        quantity = int(request.POST.get('quantity', None))
        if None in [product_id, size_id, color_id, quantity]:
            return jsonRes({
                'data': 'error',
                'msg': 'field required!'
            })
        product = Product.objects.filter(id=product_id).first()
        size = Size.objects.filter(id=size_id).first()
        color = Color.objects.filter(id=color_id).first()
        if None in [product, size, color]:
            return jsonRes({
                'data': 'error',
                'msg': 'one object not found!'
            })
        cart = Cart.objects.filter(user=request.user, complete=False).first()
        if not cart:
            cart = Cart.objects.create(user=request.user, complete=False)
        cart_item = CartItem.objects.filter(cart=cart,product=product,color=color,size=size).first()
        if not cart_item:
            cart_item = CartItem.objects.create(cart=cart,product=product,color=color,size=size)
        cart_item.quantity += quantity
        cart_item.save()
        return jsonRes({
            'data': 'success',
            'count' : int(cart.items.count())
        })

    return jsonRes({
        'data': 'error',
        'msg': 'Accept denied!'
    })
