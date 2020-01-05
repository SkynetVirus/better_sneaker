from django.db import models
from solo.models import SingletonModel
from product.models import (Product)
# Create your models here.


class TemplateConfiguration(SingletonModel):
    banner_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, default=None)
    show_banner_1 = models.BooleanField(default=True,null=True,blank=True)
    show_characteristics = models.BooleanField(default=True,null=True,blank=True)
    show_deals_featured = models.BooleanField(default=True,null=True,blank=True)
    show_popular_categories = models.BooleanField(default=True,null=True,blank=True)
    show_banner_2 = models.BooleanField(default=True,null=True,blank=True)
    # banner_2_items = models.ManyToManyField(Product)
    show_new_arrivals = models.BooleanField(default=True,null=True,blank=True)
    show_best_sellers = models.BooleanField(default=True,null=True,blank=True)
    show_trends = models.BooleanField(default=True,null=True,blank=True)
    show_latest_reviews = models.BooleanField(default=True,null=True,blank=True)
    show_viewed = models.BooleanField(default=True,null=True,blank=True)