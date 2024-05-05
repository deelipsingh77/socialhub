from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Post, Like, Comment
from django.dispatch import receiver
import os


# Create your views here.


def get_followings(user_profile):
    all_followers = user_profile.followers.all()
    all_followings = []
    for followings in all_followers:
        all_followings.append(UserProfile.objects.get(user=followings))
    return all_followings


@login_required(login_url="/login/")
def home(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

    #test code
    

    context = {
        "user": user,
        "user_profile": user_profile,
        "posts": posts,
        "comments": comments,
        "likes": likes,
        "following_profiles": all_followings,
        "all_users": all_users,
    }

    return render(request, "home.html", context)


@login_required(login_url="/login/")
def search_page(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()

    all_followings = get_followings(user_profile)
    context = {
        "user": user,
        "user_profile": user_profile,
        "all_users": all_users,
        "following_profiles": all_followings,
    }
    return render(request, "search.html", context)


@login_required(login_url="/login/")
def my_posts(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by("-pub_date")

    all_followings = get_followings(user_profile)
    context = {
        "posts": posts,
        "user_profile": user_profile,
        "user": user,
        "following_profiles": all_followings,
    }
    return render(request, "posts.html", context)


@login_required(login_url="/login/")
def create_post(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        author = user

        Post.objects.create(title=title, content=content, image=image, author=author)
        return redirect(f"/{request.user}/my_posts/")

    all_followings = get_followings(user_profile)
    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
    }
    return render(request, "create_post.html", context)


@login_required(login_url="/login/")
def delete_post(request, id):
    post = Post.objects.get(id=id)

    if post.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
        if os.path.exists(image_path):
            os.remove(image_path)

    post.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login/")
def like_post(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    is_liked = Like.objects.filter(post=post, user=user).first()

    if is_liked:
        is_liked.delete()
        post.likes_count -= 1
    else:
        Like.objects.create(user=user, post=post)
        post.likes_count += 1

    post.save()
    count = len(Like.objects.filter(post=post))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login/")
def comment_post(request, id):
    content = request.POST.get("content")
    post = Post.objects.get(id=id)
    author = request.user

    Comment.objects.create(content=content, post=post, author=author)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login/")
def follow_unfollow_user(request, username):
    to_follow = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=request.user)

    if to_follow in user_profile.followers.all():
        user_profile.followers.remove(to_follow)
    else:
        user_profile.followers.add(to_follow)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return redirect(f'/{request.user}/search/?{show_follow}')
