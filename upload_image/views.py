from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from upload_image.models import Image
from upload_image.serializer import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
