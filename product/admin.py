from django.contrib import admin
from .models import (Color, Image, Size, Product, Brand ,ThroughColorAndProduct)
# Register your models here.


class colors_inline(admin.TabularInline):
    model = Color
    extra = 1


class sizes_inline(admin.TabularInline):
    model = Size
    extra = 1


class images_inline(admin.TabularInline):
    model = Image
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [images_inline]


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
