from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Post, Like, Comment
from django.dispatch import receiver
import os
import requests


# Create your views here.
def get_followings(user_profile):
    all_followers = user_profile.followers.all()
    all_followings = []
    for followings in all_followers:
        all_followings.append(UserProfile.objects.get(user=followings))
    return all_followings


def fetch_api_data(request, type):
    api_key = "pub_436579ec8dff124afcaf5df2105bd70466ea5"
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={type}&language=en"

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url="/landing/")
def home(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all().order_by("-pub_date")
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

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


@login_required(login_url="/landing/")
def my_profile(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

    context = {
        "user": user,
        "user_profile": user_profile,
        "posts": posts,
        "comments": comments,
        "likes": likes,
        "following_profiles": all_followings,
        "all_users": all_users,
    }

    return render(request, "myprofile.html", context)


@login_required(login_url="/landing/")
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


@login_required(login_url="/landing/")
def my_posts(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by("-pub_date")
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

    all_followings = get_followings(user_profile)
    context = {
        "posts": posts,
        "user_profile": user_profile,
        "user": user,
        "following_profiles": all_followings,
        "comments": comments,
        "likes": likes,
        "all_users": all_users,
    }
    return render(request, "posts.html", context)


@login_required(login_url="/landing/")
def create_post(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        author = user

        Post.objects.create(title=title, content=content, image=image, author=author)
        return redirect(f"/{request.user}/my_posts/")

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
    }
    return render(request, "create_post.html", context)


@login_required(login_url="/landing/")
def delete_post(request, id):
    post = Post.objects.get(id=id)

    if post.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
        if os.path.exists(image_path):
            os.remove(image_path)

    post.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/landing/")
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


@login_required(login_url="/landing/")
def comment_post(request, id):
    content = request.POST.get("content")
    post = Post.objects.get(id=id)
    author = request.user

    Comment.objects.create(content=content, post=post, author=author)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/landing/")
def follow_unfollow_user(request, username):
    to_follow = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=request.user)

    if to_follow in user_profile.followers.all():
        user_profile.followers.remove(to_follow)
    else:
        user_profile.followers.add(to_follow)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return redirect(f'/{request.user}/search/?{show_follow}')


@login_required(login_url="/landing/")
def edit_profile(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        profile_pic = request.FILES.get("profile_pic")

        if not profile_pic:
            profile_pic = user_profile.profile_pic

        bio = request.POST.get("bio")
        user_profile.profile_pic = profile_pic
        user_profile.bio = bio
        user.save()
        user_profile.save()
        return redirect(f"/{request.user}/my_profile/")
    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
    }
    return render(request, "edit_profile.html", context)


@login_required(login_url="/landing/")
def notifications_page(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
    }

    return render(request, "notifications.html", context)


@login_required(login_url="/landing/")
def chat_page(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
    }
    return render(request, "chat.html", context)


@login_required(login_url="/landing/")
def others_profile_page(request, otheruser):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all().order_by("-pub_date")
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=user)
    all_followings = get_followings(user_profile)
    all_users = UserProfile.objects.all()

    other_user = User.objects.get(username=otheruser)
    others_profile = UserProfile.objects.get(user=other_user)

    context = {
        "user": user,
        "user_profile": user_profile,
        "posts": posts,
        "comments": comments,
        "likes": likes,
        "following_profiles": all_followings,
        "all_users": all_users,
        "others_profile": others_profile,
    }

    return render(request, "othersprofile.html", context)


@login_required(login_url="/landing/")
def entertainment_feeds(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)
    feeds_data = fetch_api_data(request, "entertainment")

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
        "feeds_data": feeds_data,
    }

    return render(request, "feeds.html", context)


@login_required(login_url="/landing/")
def foods_feeds(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)
    feeds_data = fetch_api_data(request, "food")

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
        "feeds_data": feeds_data,
    }

    return render(request, "foods_feeds.html", context)


@login_required(login_url="/landing/")
def education_feeds(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_users = UserProfile.objects.all()
    all_followings = get_followings(user_profile)
    feeds_data = fetch_api_data(request, "education")

    context = {
        "user": user,
        "user_profile": user_profile,
        "following_profiles": all_followings,
        "all_users": all_users,
        "feeds_data": feeds_data,
    }

    return render(request, "education_feeds.html", context)
