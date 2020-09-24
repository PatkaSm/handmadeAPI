from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer
from offer.permissions import IsAdmin, IsObjectOwnerOrAdmin


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_name='nav_categories', url_path='nav_categories')
    def get_category(self, request):
        categories = Category.objects.filter(parent__name="Wszystko").union(
            Category.objects.filter(name="Wszystko")).order_by("name")
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='categories_to_add_offer', url_path='no_core')
    def get_all_category(self, request):
        allCategories = Category.objects.filter(children__isnull=True)
        serializer = CategorySerializer(allCategories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_name='create_category', url_path='create_category')
    def create_category(self, request):
        category = CategorySerializer(data=request.data)
        self.check_object_permissions(request, category)
        if not category.is_valid():
            print(category.errors)
            return Response(data=category.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        parent = Category.objects.get(id=request.data.get('parent'))
        category.save(parent=parent)
        return Response(data=category.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'], url_name='update_category', url_path='/(?P<category_id>\d+)')
    def update_category(self, request, **kwargs):
        category = get_object_or_404(Category, id=kwargs.get('category_id'))
        if 'parent' in request.data.keys():
            parent = Category.objects.get(id=request.data.get('parent'))
            category.parent = parent
            category.save()
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(category, serializer.validated_data)
        return Response(data={'success': 'Pomyślnie edytowano kategorię!'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'nav_categories':
            self.permission_classes = [AllowAny]
        if self.action == 'categories_to_add_offer':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'update_category' or self.action == 'retrieve' \
                or self.action == 'list' or self.action == 'create_category':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
