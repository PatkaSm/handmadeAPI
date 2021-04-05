from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
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


class OfferViewSet(MultiSerializerMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Offer.objects.filter(owner__active=True)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {'price': ['gte', 'lte'], 'item__color': ['exact'], 'tag__word': ['exact'], 'gender': ['exact'],
                        'date': ['exact'], 'shipping_abroad': ['exact'], 'item__ready_in': ['exact']}
    search_fields = ['=tag__word', '=owner__nickname', '=item__name']
    ordering_fields = ['date', 'price']
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
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        if len(request.GET) < 1:
            return Response(data={'failed': 'Nie podano kategorii'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        category_name = request.GET.get('category', 'Wszystko')
        if category_name == 'Wszystko':
            subcategories_list = Category.objects.all()
        else:
            category = Category.objects.get(name=category_name)
            subcategories_list = category.subcategories()
        offers = queryset.filter(item__category__in=subcategories_list, owner__active=True)
        serializer = self.get_serializer(offers, many=True, context={'request': request})
        paginator = LimitOffsetPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(detail=False, methods=['get'], url_name='user_offers', url_path='user/(?P<user_id>\d+)/offers')
    def user_offers(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        offers = Offer.objects.filter(owner=user, owner__active=True)
        serializer = self.get_serializer(offers, many=True, context={'request': request})
        paginator = LimitOffsetPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'offers_by_category' or self.action == 'retrieve' or self.action == 'list' \
                or self.action == 'user_offers':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
