from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True, default="blank-profile.svg")
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
