from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from .forms import RegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
# from posts.models import Category
# Create your views here.

def register(request): #view đăng ký
    form = RegisterForm() 
    if request.method == 'POST': #kiểm tra phương thức nếu là post thì  thực hiện câu lệnh bên dưới
        form = RegisterForm(request.POST) #khởi tạo form mới với dữ liệu đưa vào
        if form.is_valid(): #kiểm tra nếu form hợp lệ thì thực hiện câu lệnh bên dưới
            form.save() #lưu thông tin lại
            return HttpResponseRedirect('/') #quay lại trang mặc định
    #nếu dữ liệu người dùng nhập không hợp lệ thì render form kèm lỗi
    context = {
        'form':form,
    }
    return render(request,'templates/register.html',context)

def login(request): #view đăng ký
    context = {}
    if request.method == 'POST': #kiểm tra phương thức reques có post đã được mã hóa hay không, nếu đúng thì thực hiện câu lệnh bên dưới
        username = str(request.POST['username']).strip() #láy ra username người dùng nhập
        password = str(request.POST['password']).strip() #lấy ra password người dùng nhập
        user = authenticate(request,username = username, password = password) #kiểm tra username, password và session
        if user: #nếu người dùng hợp lệ thì thực hiện câu lệnh bên dưới
            auth_login(request,user) #lưu phiên lằm việc session
            return JsonResponse({'data' : 'success'})
        else:
            return JsonResponse({
                'data' : 'error',
                'msg': 'Tên đăng nhập hoặc mật khẩu không đúng!'
            })
    else:
        return render(request,'templates/login.html',context) #render file html mới nếu phương thức bị người dùng thay đổi

# @login_required(login_url='/account/signin/') #khai báo trang điêu hướng đăng nhập
# def profile(request,username): 
#     if request.method == 'POST': #kiểm tra phương thức request
#         user_form = UserUpdateForm( 
#             request.POST,
#             instance = request.user) #khởi tạo form người dùng chứa dữ liệu update model user
#         profile_form = ProfileUpdateForm(
#             request.POST,
#             request.FILES,
#             instance = request.user.profile) #khởi tạo form hồ sơ kèm dữ liệu update model profile
#         if user_form.is_valid() and profile_form.is_valid(): #kiểm tra form có hợp lệ hay không
#             user_form.save() #lưu data update user nếu dữ liệu hợp lệ
#             profile_form.save() #lưu data profile nếu dữ liệu hợp lệ
#             request.user.profile.update_avatar() #update avata cho profile với kích thước vuông
#             messages.success(request,f'Thay đổi của bạn đã được cập nhập') #thông báo cập nhập thành công
#             # return redirect('profile/username='+username) #điều hướng người dùng về trang hiện tại(người dùng cần xem lại thông tin đã được thay đổi)
#             return redirect('/account/profile/username='+username) #điều hướng người dùng về trang hiện tại(người dùng cần xem lại thông tin đã được thay đổi)
#         else:
#             messages.error(request,f'Có lỗi xảy ra vui lòng thử lại') #thông báo lỗi nếu dữ liệu người dùng nhập không hợp lệ hoặc lỗi update
#     else:
#         user_form = UserUpdateForm(instance = request.user) #nếu phương thức bị thay đổi thì trả lại form và không nói gì
#         profile_form = ProfileUpdateForm(instance = request.user.profile) #nếu phương thức bị thay đổi thì trả lại form và không nói gì
#     context = {
#         'user':user_form,
#         'profile':profile_form,
#         # 'Categorys':Category.objects.all(),
#     }
#     return render(request,'profile.html',context)

def logout(request): #view đăng xuất
    auth_logout(request) #hủy phiên làm việc session và cache từ chối truy cập vào những lần sau
    return redirect(reverse('home:index'))

