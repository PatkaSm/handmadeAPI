from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from category.models import Category
from core.views import MultiSerializerMixin
from user.models import User
from core.permissions import IsObjectOwnerOrAdmin
from offer.models import Offer
from offer.serializer import OfferSerializer, OfferReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class OfferViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Offer.objects.filter(owner__active=True)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['price', 'date', 'favourite']
    filter_fields = ['price', 'item__color', 'item__ready_in', 'item__category__name', 'gender']
    serializers = {
        'create': OfferSerializer,
        'update': OfferSerializer,
        'partial_update': OfferSerializer,
        'user_offers': OfferReadSerializer,
        'offers_by_category': OfferReadSerializer,
        'list': OfferReadSerializer,
        'retrieve': OfferReadSerializer,
        'search': OfferReadSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], url_name='search', url_path='search')
    def search(self, request):
        word = request.GET.get('search')
        results = Offer.objects.filter(tag__word__contains=word).union(Offer.objects.filter(item__name__contains=word))
        serializer = self.get_serializer(results, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='offers_by_category', url_path='filter')
    def offers_by_category(self, request):
        if len(request.GET) < 1:
            return Response(data={'failed': 'Nie podano kategorii'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        category_name = request.GET.get('category', 'Wszystko')
        if category_name == 'Wszystko':
            subcategories_list = Category.objects.all()
        else:
            category = Category.objects.get(name=category_name)
            subcategories_list = category.subcategories()
        offers = Offer.objects.filter(item__category__in=subcategories_list, owner__active=True)
        filters = {}
        for key in request.GET.keys():
            if key != 'category':
                filters[key] = request.GET.get(key)
        offers = offers.filter(**filters)
        serializer = self.get_serializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_offers', url_path='user/(?P<user_id>\d+)/offers')
    def user_offers(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        offers = Offer.objects.filter(owner=user, owner__active=True)
        serializer = self.get_serializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'offers_by_category' or self.action == 'retrieve' or self.action == 'list'\
                or self.action == 'user_offers':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
