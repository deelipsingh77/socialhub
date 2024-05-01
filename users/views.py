from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        valid_user=authenticate(username=username,password=password)
        
        if valid_user is not None:
            login(request,valid_user)
            return redirect("home")
        else:
            messages.error(request,"Wrong username or password")
            return redirect("login")
    return render(request,"login.html")

def home(req):
    logout_url = reverse('logout')
    return HttpResponse(f"home <a href='{logout_url}'>logout</a> ")

def logout_page(request):
    logout(request)
    return redirect("login")

def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Password do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        UserProfile.objects.create(user=user)

        messages.success(request, "Registration Successful. You can now login.")
        return redirect('login')
    else:
        return render(request, 'register.html')