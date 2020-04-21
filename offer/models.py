from django.db import models

from item.models import Item
from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.item.id, filename)


choices = [('Damski','Damski'), ('Męski','Męski'),('Dziecięcy','Dziecięcy'),('Uniwersalny','Uniwersalny')]


class Offer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.ManyToManyField(Tag)
    gender = models.CharField(max_length=255, choices=choices, default='Wszyscy')
    date = models.DateField(auto_now=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

