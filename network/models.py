from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime

class User(AbstractUser):
    num_follower = models.IntegerField(default=0, blank=True)
    num_following = models.IntegerField(default=0, blank=True)
    def serialize(self):
        return {
            "username": self.username,
            "num_follower": self.num_follower,
            "num_following": self.num_following
        }

class Post(models.Model):  
    content = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    like = models.IntegerField(default=0, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "poster": self.poster.username,
            "like": self.like 
        }

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

class Follow(models.Model):
    #Person that is following another person
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    #Person that is being followed by another person
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")