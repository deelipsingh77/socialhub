from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect(f"/{request.user}/home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        valid_user = authenticate(username=username, password=password)

        if valid_user is not None:
            login(request, valid_user)
            return redirect(f"/{username}/home")
        else:
            messages.error(request, "Wrong username or password")
            return redirect("/landing/")


def logout_page(request):
    logout(request)
    return redirect("landing")


def register_page(request):
    if request.user.is_authenticated:
        return redirect(f"/{request.user}/home")
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, "Please fill all the details.")
            return redirect("landing")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("landing")

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect("landing")

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect("landing")

        user.first_name = first_name
        user.last_name = last_name
        user.save()
        UserProfile.objects.create(user=user)

        messages.success(request, "Registration Successful. You can now login.")
        return redirect("/landing/")

    return redirect("landing")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect(f"/{request.user}/home")
    return render(request, "landing-page.html")
