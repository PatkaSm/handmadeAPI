
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'city', 'image']

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

