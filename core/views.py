from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserProfile

# Create your views here.


@login_required(login_url="/login/")
def home(request, username):
    user = request.user
    data = UserProfile.objects.get(user=user)

    context = {"user": user, "data": data}

    return render(request, "home.html", context)


@login_required(login_url="/login/")
def search_page(request, username):
    user = request.user
    data = UserProfile.objects.get(user=user)

    context = {"user": user, "data": data}
    return render(request, "search.html", context)

@login_required(login_url='/login/')
def my_posts(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    