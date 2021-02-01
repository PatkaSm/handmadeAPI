from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from upload_image.models import Image
from upload_image.serializer import ImageSerializer




class ImageViewSet(mixins.CreateModelMixin,
                   GenericViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
