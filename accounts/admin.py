from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (Profile)
#Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','address','phone_number','birth_date']
    list_filter = ['birth_date']
    search_fields = ['user__username','address','phone_number']

class UserProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'
    can_delete = False
    max_num = 1
    fk_name = 'user'

class AccountUserAdmin(UserAdmin):
    from_encoding = "utf-8-sig"
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User,AccountUserAdmin) #đăng kí hiển thị profile trong admin