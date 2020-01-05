from category.models import (Category)
from .models import (TemplateConfiguration)


def categories(request):
    _ = Category.objects.filter(parent=None)
    return {
        'categories': _
    }


def home_config(request):
    _ = TemplateConfiguration.objects.get()
    return {
        'home_config': _
    }
