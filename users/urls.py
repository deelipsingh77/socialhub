from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.register_page, name="register"),
    path("landing/", views.landing_page, name="landing"),
    path("", views.landing_page, name="landing_home"),
]
