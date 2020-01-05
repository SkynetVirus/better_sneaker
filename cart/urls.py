from django.conf.urls import url
from .views import (index,remove_item,add_item)

app_name = 'cart'
urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^remove-item/$',remove_item,name='remove_item'),
    url(r'^add-item/$',add_item,name='add_item'),
]
