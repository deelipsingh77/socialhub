from django.http import HttpResponse
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
        
        if valid_user:
            login(request,valid_user)
            return redirect("home")
        else:
            messages.error(request,"Wrong username or password")
            return redirect("login")
            



    return render(request,"login.html")


def home(req):
    return HttpResponse("home <a href='/logout/'>logout</a> ")

def logout_page(request):
    logout(request)
    return redirect("login")