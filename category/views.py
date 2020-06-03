from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer
from offer.permissions import IsAdmin, IsObjectOwnerOrAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_name='nav_categories', url_path='categories')
    def get_category(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='categories_to_add_offer', url_path='categories/no_core')
    def get_all_category(self, request):
        allCategories = Category.objects.filter(children__isnull=True)
        serializer = CategorySerializer(allCategories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='all_categories', url_path='all')
    def get_all_category_with_core(self, request):
        allCategories = Category.objects.all()
        serializer = CategorySerializer(allCategories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='delete', url_path='(?P<category_id>\d+)/delete')
    def delete_category(self, request, **kwargs):
        category = get_object_or_404(Category, id=kwargs.get('category_id'))
        self.check_object_permissions(request, category)
        category.delete()
        return Response(data={'success': 'Pomyślnie usunięto kategorię!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_name='create', url_path='create')
    def create_category(self, request):
        print(request.data)
        category = CategorySerializer(data=request.data)
        self.check_object_permissions(request, category)
        if not category.is_valid():
            print(category.errors)
            return Response(data=category.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        parent = Category.objects.get(id=request.data.get('parent'))
        category.save(parent=parent)
        return Response(data=category.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'], url_name='update', url_path='(?P<category_id>\d+)/edit')
    def edit_category(self, request, **kwargs):
        print(request.data)
        category = get_object_or_404(Category, id=kwargs.get('category_id'))
        if 'parent' in request.data.keys():
            parent = Category.objects.get(id=request.data.get('parent'))
            category.parent = parent
            category.save()
        request.data.pop('parent')
        serializer = CategorySerializer(category, data= request.data, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(category, serializer.validated_data)
        return Response(data={'success': 'Pomyślnie edytowano kategorię!'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'nav_categories':
            self.permission_classes = [AllowAny]
        if self.action == 'categories_to_add_offer':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'delete' or self.action == 'create' or self.action == 'update' \
                or self.action == 'all_categories':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
