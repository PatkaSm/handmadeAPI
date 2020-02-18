
from rest_framework import serializers

from item.models import Item
from item.serializer import ItemSerializer
from offer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Offer
        fields = ['owner', 'item', 'amount', 'price', 'tag']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        offer = Offer.objects.create(**validated_data)
        Item.objects.create(**item_data)
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


