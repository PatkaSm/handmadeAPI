from rest_framework import serializers

from upload_image.models import Image, PostImage


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'offer', 'img']


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ['id', 'post', 'img']