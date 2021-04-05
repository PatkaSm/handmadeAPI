from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer
from core.permissions import IsAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_name='nav_categories', url_path='nav_categories')
    def nav_categories(self, request):
        categories = Category.objects.filter(parent__name="Wszystko").union(
            Category.objects.filter(name="Wszystko")).order_by("name")
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='categories_to_add_offer', url_path='no_core')
    def categories_to_add_offer(self, request):
        all_categories = Category.objects.filter(children__isnull=True)
        serializer = CategorySerializer(all_categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='categories_core', url_path='core')
    def core_categories(self, request):
        all_categories = Category.objects.filter(parent__name='Wszystko')
        serializer = CategorySerializer(all_categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'nav_categories':
            self.permission_classes = [AllowAny]
        if self.action == 'categories_to_add_offer' or self.action == 'categories_core':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve' or\
                self.action == 'create' or self.action == 'destroy':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
