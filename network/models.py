from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self")
    followed_by = models.ManyToManyField("self")

class Post(models.Model):
    content = models.TextField(default="post")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+"
    )
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, )
