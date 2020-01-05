from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
import re


class RegisterForm(forms.Form): #form đăng kí tài khoản
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Tên đăng nhập'})) #trường username
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'Địa chỉ Email'})) #trường email
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Mật khẩu'})) #trường mật khẩu
    retype_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Nhập lại mật khẩu'})) #trường nhập lại mật khẩu

    def clean_username(self): #hàm kiểm tra input username có hợp lệ hay không
        username = self.cleaned_data['username'] #lấy input username
        if not re.search(r'^\w+$', username): #so khớp chuỗi với biển thức chính quy 
            raise forms.ValidationError("Tên đăng nhập không hợp lệ") #trả về lỗi nếu username chứa các ký tự lạ
        try:
            User.objects.get(username=username) #kiểm tra username đã tồn tại hay chưa
        except ObjectDoesNotExist: #nếu username không tồn tại thì 
            return username #trả về user name
        raise forms.ValidationError("Tài khoản đã tồn tại") #ngược lại thì thông báo lỗi tài khoản đã tồn tại

    def clean_retype_password(self): #hàm kiểm tra input password và nhập lại pass
        if 'password' in self.cleaned_data: #kiểm tra field password đã nhập hay chưa
            password = self.cleaned_data['password'] #lấy ra password
            retype_password = self.cleaned_data['retype_password'] #láy ra retype_password
            if password == retype_password and password: #so sánh password với retype_password và password 
                return password #trả về password sau khi đã được kiểm tra
        raise forms.ValidationError("Mật khẩu không hợp lệ") #ném ra lỗi password

    def clean_email(self): #hàm kiểm tra input email
        email = self.cleaned_data['email'] #lấy ra email
        try:
            User.objects.get(email=email) #thử kiểm tra email đã từng được đăng ký hay chưa
        except ObjectDoesNotExist:
            return email #nếu chưa thì trả về email
        raise forms.ValidationError("Email đã được sử dụng") #ném ra lỗi nếu email đã được sử dụng

    def save(self): #hàm lưu lại thông tin đăng ký
        User.objects.create_user(
            username= self.cleaned_data['username'],
            email= self.cleaned_data['email'],
            password= self.cleaned_data['password']
        )


class UserUpdateForm(forms.ModelForm): #form user kế thừa từ model với các trường được phép hiển thị được khai báo trong fields
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):#form prifile kế thừa từ model với các trường được phép hiển thị được khai báo trong fields
    class Meta:
        model = Profile
        fields = [ 'phone_number', 'address', 'birth_date']
    
