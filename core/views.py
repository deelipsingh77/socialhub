from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Post
from django.dispatch import receiver
import os

# Create your views here.


@login_required(login_url="/login/")
def home(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    context = {"user": user, "user_profile": user_profile}

    return render(request, "home.html", context)


@login_required(login_url="/login/")
def search_page(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    context = {"user": user, "user_profile": user_profile}
    return render(request, "search.html", context)

@login_required(login_url='/login/')
def my_posts(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    posts=Post.objects.filter(author=user).order_by('-pub_date')

    context={
        "posts":posts,
        "user_profile":user_profile,
        "user":user
    }
    return render(request,"posts.html",context)

@login_required(login_url='/login/')
def create_post(request,username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method=="POST":
        title=request.POST.get('title')        
        content=request.POST.get('content')
        image=request.FILES.get('image')
        author=user

        Post.objects.create(title=title,content=content,image=image,author=author)



    context={"user":user,"user_profile":user_profile}
    return render(request,"create_post.html",context)


@login_required(login_url='/login/')
def delete_post(request,id):
    post = Post.objects.get(id=id)
    
    if post.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
        if os.path.exists(image_path):
            os.remove(image_path)

    post.delete()
    return redirect(f'/{request.user}/my_posts')