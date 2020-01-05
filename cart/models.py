from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from product.models import (Product, Color, Size)
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.product.name

    @property
    def total(self):
        return self.product.price_after_sale() * self.quantity


class Cart(models.Model):
    FIELD_ID_NAME = 'CartID'
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(Product, through=CartItem)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __unicode__(self):
        return str(self.id)

    @property
    def count(self):
        return self.cartitem_set.count()

    @property
    def cart_item(self):
        return CartItem.objects.filter(cart=self)

    @property
    def cart_price(self):
        price_total = 0
        for item in CartItem.objects.filter(cart=self):
            price_total += item.total
        return price_total

    @property
    def total_count(self):
        cart_count = 0
        for item in self.cartitem_set.all():
            cart_count += item.quantity
        return cart_count
