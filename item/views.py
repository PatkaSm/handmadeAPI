from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from offer.models import Offer
from .models import Item
from .serializer import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'], url_name='colors', url_path='colors')
    def get_item_properties(self, request):
        data = {
            'colors': Item.Colors.choices,
            'ready_in': Item.Days.choices,
            'gender': Offer.GenderType.choices
        }
        return Response(data=data, status=200)