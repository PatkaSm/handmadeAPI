from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from upload_image.models import Image
from upload_image.serializer import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(methods=['post'], detail=False, url_name='create', url_path=r'create')
    def create_img(self, request):
        print(request.data)
        images = []
        data = dict(request.data.lists())
        offer_data = data['offer']
        img_data = data['img']
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

        return Response(data={'wszystko ok'}, status=status.HTTP_201_CREATED)


