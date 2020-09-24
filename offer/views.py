from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from category.models import Category
from user.models import User
from .permissions import IsObjectOwnerOrAdmin
from offer.models import Offer
from offer.serializer import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.filter(owner__active=True)
    serializer_class = OfferSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'date', 'favourite']

    # filterset_fields = ['price', 'item__color', 'item__ready_in', 'item__category__name', 'gender']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], url_name='search', url_path='search')
    def search(self, request):
        word = request.GET.get('search')
        results = Offer.objects.filter(tag__word__contains=word).union(Offer.objects.filter(item__name__contains=word))
        serializer = OfferSerializer(results, many=True, context={'request': request})
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
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_offers', url_path='user/(?P<user_id>\d+)/offers')
    def user_offers(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        offers = Offer.objects.filter(owner=user, owner__active=True)
        serializer = OfferSerializer(offers, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'user_offers' or self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'offers_by_category' or self.action == 'Retrieve' or self.action == 'list':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
