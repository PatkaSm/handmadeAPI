from django.db import models
from rest_framework.utils import json


from item.models import Item
from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.item.id, filename)


class Offer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.ManyToManyField(Tag)

    @staticmethod
    def get_offer_data(request, offers):
        data = []
        for offer in offers:
            images = []
            image = upload_image.models.Image.objects.filter(offer=offer.id)
            for img in image:
                serializer = upload_image.serializer.ImageSerializer(img)
                images.append(json.dumps(str(serializer.data['img'])))
            if not request.user.is_authenticated:
                is_favourite = False
            else:
                is_favourite = favourites.models.Favourite.objects.filter(user=request.user, offer=offer).exists()
            data.append({
                'id': offer.id,
                'owner': {
                    'id': offer.owner_id,
                    'email': offer.owner.email,
                    'nickname': offer.owner.nickname,
                    'first_name': offer.owner.first_name,
                    'last_name': offer.owner.first_name,
                },
                'item': {
                    'id': offer.item_id,
                    'name': offer.item.name,
                    'category': offer.item.category,
                },
                'amount': offer.amount,
                'price': offer.price,
                'tag': list(offer.tag.all().values()),
                'image': images,
                'is_favourite': is_favourite
            })
        return data


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)


import favourites.models, upload_image.models, upload_image.serializer
