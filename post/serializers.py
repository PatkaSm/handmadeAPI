from rest_framework import serializers

from groups.serializers import GroupSerializer
from posts.models import Post, Comment
from users.serializers import UserSerializer

from upload_image.models import PostImage
from upload_image.serializer import PostImageSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    images = serializers.SerializerMethodField()

    def get_owner(self, instance):
        return UserSerializer(instance=instance.owner, context=self.context).data

    class Meta:
        model = Post
        fields = ['id', 'owner', 'content', 'date_posted', 'image']
        read_only_fields = ['owner']

    def get_images(self, obj):
        post_images = PostImage.objects.filter(offer=obj.id)
        serializer = PostImageSerializer(post_images, many=True)
        images = []
        for offers in serializer.data:
            images.append(('http://' + self.context['request'].get_host() + offers['img']))
        return images

