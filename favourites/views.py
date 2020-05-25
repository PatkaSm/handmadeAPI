from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.models import Favourite
from favourites.serializer import FavouriteSerializer
from offer.models import Offer


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    @action(detail=False, methods=['post'], url_name='add_or_remove', url_path='add/(?P<offer_id>\d+)')
    def add_or_remove(self, request, **kwargs):
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        try:
            fav_offer = Favourite.objects.get(offer=offer, user=request.user)
        except Favourite.DoesNotExist:
            Favourite.objects.create(offer=offer, user=request.user)
            return Response(data={'success': 'Dodano ofertę do ulubionych!'}, status=status.HTTP_201_CREATED)
        fav_offer.delete()
        return Response(data={'success': 'Usunięto ofertę z ulubionych!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_fav_offerts', url_path='my_favourites')
    def my_favourites(self, request):
        fav_offers = Favourite.objects.filter(user=request.user)
        serializer = FavouriteSerializer(fav_offers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'my_favourites' or self.action == 'add_or_remove':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]