from django.db import models

from category.models import Category
from upload_image.models import Image
from user.models import User


class Post(models.Model):
    title = models.TextField(max_length=550)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    content = models.TextField(max_length=5555)
    gallery = models.ManyToManyField(Image, blank=True, related_name="post_gallery")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)