from django.db import models

from item.models import Item
from tag.models import Tag
from upload_image.models import Image
from user.models import User


def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.item.id, filename)


class Offer(models.Model):
    class GenderType(models.TextChoices):
        WOMAN = "woman", "Damski"
        MAN = "man", "Męski"
        KID = "dziecięcy", "Dziecięcy"
        UNISEX = "uniwersalny", "Uniwersalny"

    class ShippingAbroad(models.TextChoices):
        TRUE = "true", "Tak"
        FALSE = "false", "Nie"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    tag = models.ManyToManyField(Tag)
    gender = models.CharField(max_length=255, choices=GenderType.choices, default='Wszyscy')
    gallery = models.ManyToManyField(Image, null=True, blank=True, related_name="gallery")
    date = models.DateField(auto_now=True)
    shipping_abroad = models.CharField(choices=ShippingAbroad.choices, max_length=5)



