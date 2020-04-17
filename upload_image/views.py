from django.shortcuts import render
from rest_framework import viewsets

from upload_image.models import Image
from upload_image.serializer import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

