from django.db import models

from offer.models import Offer
from post.models import Post


def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.id, filename)


class Image(models.Model):
    img = models.ImageField(null=True, blank=True, max_length=None, upload_to=upload_location)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, blank=None)


class PostImage(models.Model):
    img = models.ImageField(null=True, blank=True, max_length=None, upload_to=upload_location)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=None)
