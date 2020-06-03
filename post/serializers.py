from rest_framework import serializers

from post.models import Post
from upload_image.models import PostImage
from upload_image.serializer import PostImageSerializer
from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    images = serializers.SerializerMethodField()
    host = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'owner', 'content', 'date_posted', 'images', 'host']
        read_only_fields = ['owner']

    def get_host(self, obj):
        host = 'http://' + self.context['request'].get_host()
        return host

    def get_images(self, obj):
        post_images = PostImage.objects.filter(post=obj.id)
        serializer = PostImageSerializer(post_images, many=True)
        return serializer.data

