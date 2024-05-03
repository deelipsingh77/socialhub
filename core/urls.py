from django.urls import path
from . import views


urlpatterns = [
    path("<username>/home/", views.home, name="home"),
    path("<username>/search/", views.search_page, name="search"),
    path("<username>/my_posts/", views.my_posts, name="my_posts"),
    path("<username>/create_post/", views.create_post, name="create_posts"),
    path("<id>/delete_post/", views.delete_post, name="delete_post"),

]
