from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer
from upload_image.models import Image
from upload_image.serializer import ImageSerializer
from user.models import User
from user.serializer import UserSerializer
from .permissions import IsObjectOwnerOrAdmin
from offer.models import Offer
from offer.serializer import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.filter(owner__active=True)
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['tag__word', 'item__name']
    ordering_fields = ['price', 'date']
    filterset_fields = ['price', 'item__color', 'item__ready_in']

    @action(detail=False, methods=['post'], url_name='create', url_path='create')
    def create_offer(self, request):
        offer_serializer = OfferSerializer(data=request.data, context={'request': request})
        if not offer_serializer.is_valid():
            return Response(data=offer_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        offer_serializer.save(owner=request.user)
        return Response(data=offer_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='detail', url_path='offer/detail/(?P<offer_id>\d+)')
    def offer_detail(self, request, **kwargs):
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        serializer = OfferSerializer(offer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_name='update', url_path='offer/(?P<offer_id>\d+)/edit')
    def update_offer(self, request, **kwargs):
        offer = Offer.objects.get(id=kwargs.get('offer_id'))
        serializer = OfferSerializer(offer, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(offer, serializer.validated_data)
        return Response(data={'success': 'Pomyślnie zapisano zmiany!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='delete_offer', url_path='offer/(?P<offer_id>\d+)/delete')
    def delete_offer(self, request, **kwargs):
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(data={'success': 'Pomyślnie usunięto ofertę'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='offers_by_category', url_path='filter')
    def offers_by_category(self, request):
        if len(request.GET) < 1:
            return Response(data={'failed': 'Nie podano kategorii'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        category_name = request.GET['category']
        offers = Offer.objects.filter(item__category__name=category_name, owner__active=True)
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_offers', url_path='user/(?P<user_id>\d+)/offers')
    def user_offers(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        offers = Offer.objects.filter(owner=user, owner__active=True)
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'user_offers' or self.action == 'update_offer' or self.action == 'create_offer':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete_offer':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'offers_by_category' or self.action == 'offer_detail':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]


