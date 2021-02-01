from rest_framework import serializers
from post.models import Post
from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'owner', 'content', 'date_posted', 'gallery' 'images']
        read_only_fields = ['owner']



