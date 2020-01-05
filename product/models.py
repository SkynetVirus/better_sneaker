from django.db import models
from category.models import Category
from django.dispatch import receiver
from django.db.models.signals import post_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import (MinValueValidator, MaxValueValidator)
# Create your models here.


class Size(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    centimet = models.FloatField(default=0.0, null=True, blank=False)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    html = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, max_length=255, blank=True)
    image = models.ImageField(
        upload_to='brand/images/%Y/%m/%d', null=True)  # hình hiển thị

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True,
                            blank=True, default=None)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    # images = models.ManyToManyField(Image, related_name='images')
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    dess = RichTextUploadingField(null=True, blank=True,
                                  default=None, verbose_name='description')
    price = models.FloatField(default=0.0, null=True, blank=False)
    sale = models.IntegerField(default=0, null=True, blank=False, validators=[
                               MinValueValidator(0), MaxValueValidator(100)])
    view_counter = models.IntegerField(default=0, null=True, blank=True)
    rated = models.IntegerField(default=0, validators=[MaxValueValidator(
        5), MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return self.name

    def price_after_sale(self):
        return self.price - (self.price * self.sale / 100)

    @property
    def default_image(self):
        return Image.objects.filter(product=self, default=True).first()

    @property
    def another_images(self):
        return Image.objects.filter(product=self, default=False)


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True)
    thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    default = models.BooleanField(default=False, null=True, blank=True)
    display = models.BooleanField(default=True, null=True, blank=True)


class ThroughColorAndProduct(models.Model):
    a = models.ForeignKey(Color, on_delete=models.CASCADE)
    b = models.ForeignKey(Product, on_delete=models.CASCADE)


def create_slug_product(instance, new_slug=None):  # hàm tạo slug fild
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_product(instance, new_slug=new_slug)
    return slug


def create_slug_brand(instance, new_slug=None):  # hàm tạo slug fild
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Brand.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_brand(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Product)
def product_create_or_update(sender, instance, *args, **kargs):
    if not instance.slug:
        instance.slug = create_slug_product(instance)


@receiver(pre_save, sender=Brand)
def brand_create_or_update(sender, instance, *args, **kargs):
    if not instance.slug:
        instance.slug = create_slug_brand(instance)
