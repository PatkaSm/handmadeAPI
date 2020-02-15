from django.contrib.auth.models import User
from django.db import models
from item.models import Item


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
