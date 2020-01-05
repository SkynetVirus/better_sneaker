from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.

# class DeliveryAddress(models.Model):
#     pass


class Profile(models.Model):  # class hồ sơ người dúng
    # khai báo quan hệ 1-1 với class user tự động xóa profile nếu người dùng bị xóa
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FEMALE = "FEMA"
    MALE = "MALE"
    SEX_CHOICE = [
        (FEMALE, "Female"),
        (MALE, "Male")
    ]

    sex = models.CharField(max_length=4, blank=False,
                           null=True, choices=SEX_CHOICE)

    phone_number = models.CharField(max_length=11, null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):  # mặc định trả về tên người dùng user.username <-> profile
        return self.user.username


@receiver(post_save, sender=User)  # bắt tín hiệu lưu profile
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # nếu tín hiệu là tạo bài mới thì thực hiện câu lệnh dưới
        # tạo ra hồ sơ trống với user = user truyền vào
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
