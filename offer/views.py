from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response

from upload_image.models import Image
from upload_image.serializer import ImageSerializer
from user.models import User
from .permissions import IsObjectOwnerOrAdmin
from offer.models import Offer
from offer.serializer import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.filter(owner__active=True)
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['tag__word', 'item__name']
    ordering_fields = ['price', 'date']
    filterset_fields = ['price', 'item__color', 'item__ready_in', 'item__shipping_abroad']

    @action(detail=False, methods=['post'], url_name='create', url_path='create')
    def create_offer(self, request):
        offer_serializer = OfferSerializer(data=request.data['offer'])
        if not offer_serializer.is_valid():
            return Response(data=offer_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        offer = offer_serializer.save(owner=request.user, context={'request': request})
        image_serializer = ImageSerializer(data=request.data['image'])
        if not image_serializer.is_valid():
            return Response(data=image_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        image_serializer.save(offer=offer)
        data = [offer_serializer.data, image_serializer.data]
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='detail', url_path='offer/detail/(?P<offer_id>\d+)')
    def offer_detail(self, request, **kwargs):
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        serializer = OfferSerializer(offer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_name='update', url_path='offer/update/(?P<offer_id>\d+)')
    def update_offer(self, request, **kwargs):
        offer_data = request.data['offer']
        offer = Offer.objects.get(id=kwargs.get('offer_id'))
        serializer = OfferSerializer(offer, data=offer_data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        images = Image.objects.filter(offer=offer)
        images_data = request.data['images']
        img_serializer = ImageSerializer(images, data = images_data, partial=True, many=True)
        if not img_serializer.is_valid():
            return Response(data=img_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(offer, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='delete_offer', url_path='offer/delete/(?P<offer_id>\d+)')
    def delete_offer(self, request, **kwargs):
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(data={'success': 'Pomyślnie usunięto ofertę'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='offers_by_category', url_path='filter')
    def offers_by_category(self, request):
        if len(request.GET) < 1:
            return Response(data={'failed': 'Nie podano kategorii'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        category = request.GET['category']
        offers = Offer.objects.filter(item__category__name=category, owner__active=True)
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return JsonResponse(data=serializer.data, safe=False)

    @action(detail=False, methods=['get'], url_name='user_offers', url_path='user/(?P<user_id>\d+)/offers')
    def user_offers(self, request, **kwargs):
        user = get_object_or_404(User.objects.filter(id=kwargs.get('user_id')))
        offers = Offer.objects.filter(owner=user, owner__active=True)
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return JsonResponse(data=serializer.data, safe=False)


    def get_permissions(self):
        if self.action == 'user_offers' or self.action == 'update_offer' or self.action == 'create_offer':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete_offer':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'offers_by_category' or self.action == 'offer_detail':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]



