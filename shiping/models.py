from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DeliveryAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False)

    address = models.CharField(max_length=500, null=True, blank=False)

    phone = models.CharField(max_length=10, null=True, blank=True)

    default = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.address
    