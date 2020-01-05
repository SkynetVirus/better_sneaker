from django.conf.urls import url
from .views import (index,contact)

app_name = 'home'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'index/$', index, name='index'),
    url(r'contact/$', contact, name='contact'),
]
