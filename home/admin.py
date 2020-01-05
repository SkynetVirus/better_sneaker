from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import (TemplateConfiguration)
# Register your models here.
admin.site.register(TemplateConfiguration, SingletonModelAdmin)