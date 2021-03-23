from rest_framework import serializers
from post.models import Post
from upload_image.serializer import ImageSerializer
from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'owner', 'content', 'date_posted', 'gallery']
        read_only_fields = ['owner']


class PostReadSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    gallery = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'owner', 'content', 'date_posted', 'gallery']
        read_only_fields = ['owner']