from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item, COLORS
from .serializer import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'], url_name='colors', url_path='colors')
    def get_colors(self, request):
        colors = []
        for color in COLORS:
            colors.append(color[0])
        return Response(data=colors, status=200)