
from rest_framework import serializers

from item.models import Item
from item.serializer import ItemSerializer
from offer.models import Offer
from tag.models import Tag
from tag.serializer import TagSerializer


class OfferSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    tag = TagSerializer()

    class Meta:
        model = Offer
        fields = ['owner', 'item', 'amount', 'price', 'tag']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        tags_data = validated_data.pop('tag')
        item = Item.objects.create(**item_data)
        offer = Offer.objects.create(item=item, **validated_data)
        for tag_data in tags_data:
            Tag.objects.create(offer=offer, **tag_data)
        return offer

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        item = instance.item

        instance.amount = validated_data.get('amount', instance.amount)
        instance.price = validated_data.get('price', instance.price)
        instance.tag = validated_data.get('teg', instance.tag)
        instance.save()

        item.name = item_data.get('name', item.name)
        item.category = item_data.get('category', item.category)
        item.save()

        return instance


