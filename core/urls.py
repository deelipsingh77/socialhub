from django.urls import path
from . import views


urlpatterns = [
    path("<username>/home/", views.home, name="home"),
    path("<username>/search/", views.search_page, name="search"),
    path("<username>/my_profile/", views.my_profile, name="my_profile"),
    path("<username>/my_posts/", views.my_posts, name="my_posts"),
    path("<username>/create_post/", views.create_post, name="create_posts"),
    path("<id>/delete_post/", views.delete_post, name="delete_post"),
    path("<id>/like_post/", views.like_post, name="like_post"),
    path("<id>/comment_post/", views.comment_post, name="comment_post"),
    path("<username>/follow_user/", views.follow_unfollow_user, name="follow_user"),
    path("<username>/edit_profile/", views.edit_profile, name="edit_profile"),
    path("<username>/notifications/", views.notifications_page, name="notifications_page"),
    path("<username>/chat/", views.chat_page, name="chat_page"),
    path("<otheruser>/others_profile_page/", views.others_profile_page, name="others_profile_page"),
    path("<username>/entertainment_feeds/", views.entertainment_feeds, name="entertainment_feeds"),
    path("<username>/foods_feeds/", views.foods_feeds, name="foods_feeds"),
    path("<username>/education_feeds/", views.education_feeds, name="education_feeds"),

]
