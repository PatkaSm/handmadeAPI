from django.db import models

from user.models import User


class Post(models.Model):
    title = models.TextField(max_length=550)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=5555)
    date_posted = models.DateTimeField(auto_now_add=True)