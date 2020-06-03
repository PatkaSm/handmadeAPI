from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from upload_image.models import Image, PostImage
from upload_image.serializer import ImageSerializer, PostImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(methods=['post'], detail=False, url_name='create', url_path=r'create')
    def create_img(self, request):
        images = []
        offer_data = request.data.getlist('offer')
        img_data = request.data.getlist('img')
        for image in img_data:
            img = {
                'offer': offer_data[0],
                'img': image
                }
            images.append(img)
        for img in images:
            serializer = ImageSerializer(data=img)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
        return Response(data={'Dodano zdjęcia'}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_name='get', url_path=r'get/(?P<offer_id>\d+)')
    def get(self, request, **kwargs):
        images = Image.objects.filter(offer_id=kwargs.get('offer_id'))
        serializer = ImageSerializer(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer()
    parser_classes = (MultiPartParser, FormParser)

    @action(methods=['post'], detail=False, url_name='create', url_path=r'create')
    def create_img(self, request):
        images = []
        post_data = request.data.getlist('post')
        img_data = request.data.getlist('img')
        for image in img_data:
            img = {
                'post': post_data[0],
                'img': image
                }
            images.append(img)
        for img in images:
            serializer = PostImageSerializer(data=img)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
        return Response(data={'Dodano zdjęcia'}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_name='get', url_path=r'get/(?P<post_id>\d+)')
    def get(self, request, **kwargs):
        images = PostImage.objects.filter(post_id=kwargs.get('post_id'))
        serializer = PostImageSerializer(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)