from django.contrib.auth.models import User
from django.db import models
from item.models import Item
from tag.models import Tag


class Offer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(Tag)
