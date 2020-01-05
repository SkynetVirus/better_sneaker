from django.shortcuts import render, get_object_or_404
from .models import (Blog)

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request,'templates/blog.html',{'blogs':blogs})

def detail(request,slug):
    blog = get_object_or_404(Blog,slug=slug)
    return render(request,'templates/blog_single.html',{'instance': blog})