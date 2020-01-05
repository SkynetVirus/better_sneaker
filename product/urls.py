from django.conf.urls import url
from .views import (detail, index)

app_name = 'product'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'(?P<slug>[-\w]+)/$', detail, name='detail')
]
