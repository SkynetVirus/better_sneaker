from django.db import models
from django.utils.text import slugify
from django.db.models.signals import  pre_save
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Blog(models.Model):  # lớp bài đăng
    slug = models.SlugField(unique=True, null=True, max_length=255, blank=True) # trường slug, tạo url cho phép người dùng có thể đọc được
    title = models.TextField(null=True, blank=False) # tiêu đề bài đăng
    content = RichTextUploadingField(null=True, blank=False) #nội dung chính
    image = models.ImageField(upload_to='blog/images/%Y/%m/%d', null=True) #hình hiển thị

    def __str__(self):
        return self.title
    

def create_slug(instance, new_slug=None): #hàm tạo slug fild
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *agrs, **kwargs): #bắt tín hiệu lưu bài đăng
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Blog)