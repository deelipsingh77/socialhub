from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/{{request.user}}/home")
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
        return redirect("/{{request.user}}/home")
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if (
            first_name
            and last_name
            and username
            and email
            and password
            and confirm_password
        ):
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        else:
            messages.error(request, "Please fill all the deatails !!!")
            return redirect("register")

        UserProfile.objects.create(user=user)

        messages.success(request, "Registration Successful. You can now login.")
        return redirect("/landing/")
    


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("/{{request.user}}/home")
    return render(request, 'landing-page.html')