from django.urls import path
from . import views


urlpatterns = [
    path("<username>/home/",views.home,name="home"),
    path("<username>/search/",views.search_page,name="search"),
]


