from rest_framework import serializers
from favourites.models import Favourite
from item.models import Item
from item.serializer import ItemSerializer
from offer.models import Offer
from tag.models import Tag
from tag.serializer import TagSerializer
from upload_image.models import Image
from upload_image.serializer import ImageSerializer
from user.serializer import UserSerializer


class OfferSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    tag = TagSerializer(many=True)
    images = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Offer
        fields = ['id', 'owner', 'item', 'price', 'tag', 'gender', 'description', 'images', 'date', 'is_favourite',
                  'liked_by']
        read_only_fields = ['owner']

    def get_images(self, obj):
        offer_images = Image.objects.filter(offer=obj.id)
        serializer = ImageSerializer(offer_images, many=True)
        images = []
        for img in serializer.data:
            images.append(('http://' + self.context['request'].get_host() + img['img']))
        return images

    def get_is_favourite(self, obj):
        if self.context['request'].user.is_authenticated:
            is_favourite = Favourite.objects.filter(offer=obj.id, user=self.context['request'].user)
            if is_favourite.exists():
                return True
        return False

    def get_liked_by(self, obj):
        users = []
        is_favourite = Favourite.objects.filter(offer=obj.id).select_related('user')
        likes = is_favourite.count()
        for fav in is_favourite:
            users.append(fav.user.nickname)
        data = {
            'users': users,
            'likes': likes
        }
        return data

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        tags_data = validated_data.pop('tag')
        item = Item.objects.create(**item_data)
        offer = Offer.objects.create(item=item, **validated_data)
        for tag_data in tags_data:
            used_tag = Tag.objects.filter(word=tag_data['word'])
            if used_tag.exists():
                offer.tag.add(used_tag[0])
            else:
                tag = Tag.objects.create(**tag_data)
                offer.tag.add(tag)
        return offer

    def update(self, instance, validated_data):
        if 'item' in validated_data.keys():
            item_data = validated_data.pop('item')
            item = instance.item

            item.name = item_data.get('name', item.name)
            item.category = item_data.get('category', item.category)
            item.color = item_data.get('color', item.color)
            item.ready_in = item_data.get('ready_in', item.ready_in)
            item.save()

        if 'tag' in validated_data.keys():
            tags_data = validated_data.pop('tag')
            instance.tag.clear()

            for tag_data in tags_data:
                tag = Tag.objects.create(**tag_data)
                instance.tag.add(tag)

        instance.gender = validated_data.get('gender', instance.gender)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        return instance
