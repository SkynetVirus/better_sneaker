from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    slug = models.SlugField(max_length=255, unique=True,
                            null=True, blank=True)

    def __str__(self):
        return self.name

def create_slug(instance, new_slug=None):  # hàm tạo slug fild
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Category.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Category)
def category_create_or_update(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
