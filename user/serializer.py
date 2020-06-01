
from rest_framework import serializers
from rest_framework.fields import ImageField

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'city', 'image',
                  'admin']
        extra_kwargs = {'password': {'write_only': True}}

    def get_image(self, obj):
        return ('http://' + self.context['request'].get_host() + obj.image.url)

    def create(self, validates_data):
        return User.objects.create_user(**validates_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('nickname', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.image = validated_data.get('image', instance.image)
        if validated_data.get('password'):
            instance.set_password(raw_password=validated_data.get('password'))
        instance.save()
        return instance

