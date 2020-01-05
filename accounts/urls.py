from django.conf.urls import url
from .views import (register,login,logout)

app_name = 'accounts'
urlpatterns = [
    # địa chỉ url điều hướng vào view đăng ký
    url(r'register/', register, name='register'),
    # địa chỉ url điều hướng vào view đăng nhập
    url(r'login/', login, name='login'),
    # địa chỉ url điều hướng vào view đăng xuất
    url(r'logout/', logout, name='logout'),
]
