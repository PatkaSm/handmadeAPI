from django.conf import settings
from django.db import models
from item.models import Item
from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "item-%s/%s" %(instance.id, filename)


class Offer(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, blank=True, max_length=None, upload_to=upload_location)

    # class OfferManager(models.Manager):
    #     def create(self, owner, name, category, amount, price, tag):
    #         item = Item(name=name, category=category)
    #         item.save()
    #         offer = Offer(
    #             owner=owner,
    #             item=item,
    #             amount=amount,
    #             price=price,
    #             tag=tag
    #         )
    #         offer.save()
    #
    #         return offer

    # def create(self, validated_data):
    #     return Offer.objects.create(
    #         owner=validated_data['owner'],
    #         name=validated_data['item']['name'],
    #         category=validated_data['item']['category'],
    #         price=validated_data['price'],
    #         amount=validated_data['amount'],
    #         tag=validated_data['tags']
    #     )
