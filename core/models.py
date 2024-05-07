from django.db import models
from django.contrib.auth.models import User
import os
import uuid


def rename_image(instance, filename):
    upload_to = "posts/"
    ext = filename.split(".")[-1]  # Get the file extension
    new_filename = f"{uuid.uuid4()}.{ext}"  # Rename with post ID
    return os.path.join(upload_to, new_filename)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=rename_image, blank=True)
    # video_url = models.URLField(blank=True)  # Optional video URL field
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
