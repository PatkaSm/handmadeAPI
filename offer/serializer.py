from rest_framework import serializers

from item.models import Item
from item.serializer import ItemSerializer
from offer.models import Offer, Comment
from tag.models import Tag
from tag.serializer import TagSerializer
from upload_image.models import Image


class OfferSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    tag = TagSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['owner', 'item', 'amount', 'price', 'tag']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        tags_data = validated_data.pop('tag')
        item = Item.objects.create(**item_data)
        offer = Offer.objects.create(item=item, **validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.create(**tag_data)
            offer.tag.add(tag)
        return offer

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        item = instance.item
        tags_data = validated_data.pop('tag')
        tag = instance.tag

        instance.amount = validated_data.get('amount', instance.amount)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        for tag_data in tags_data:
            tag.word = tags_data.get('word', tag_data.tag)
        tag.save()
        item.name = item_data.get('name', item.name)
        item.category = item_data.get('category', item.category)
        item.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'offer', 'content', 'date']
