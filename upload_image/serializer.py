from rest_framework import serializers

from upload_image.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ["id", "img"]
        read_only_fields = ["id"]
