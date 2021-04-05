
from rest_framework import serializers
from rest_framework.fields import ImageField

from offer.models import Offer
from post.models import Post
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'first_name', 'last_name', 'phone_number', 'city', 'image',
                  'admin', 'active', 'offers', 'posts']
        read_only_fields = ['admin']
        extra_kwargs = {'password': {'write_only': True}}

    def get_offers(self, obj):
        user_offers = Offer.objects.filter(owner=obj.id)
        return len(user_offers)

    def get_posts(self, obj):
        user_posts = Post.objects.filter(owner=obj.id)
        return len(user_posts)

    def create(self, validates_data):
        return User.objects.create_user(**validates_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.active = validated_data.get('active', instance.active)
        instance.image = validated_data.get('image', instance.image)
        # if validated_data.get('password'):
        #     instance.set_password(raw_password=validated_data.get('password'))
        instance.save()
        return instance


class LoggedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'first_name', 'last_name', 'admin', 'active', 'image']
        read_only_fields = ['admin']
