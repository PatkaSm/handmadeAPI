from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from category.models import Category
from category.serializer import CategorySerializer
from offer.permissions import IsAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_name='categories', url_path='categories')
    def get_category(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(data=serializer.data, status=200, safe=False)

    @action(detail=False, methods=['get'], url_name='categories', url_path='all')
    def get_all_category(self, request):
        allCategories = Category.objects.filter(children__isnull=True)
        serializer = CategorySerializer(allCategories, many=True)
        return JsonResponse(data=serializer.data, status=200, safe=False)

    def get_permissions(self):
        if self.action == 'delete' or self.action == 'create' or self.action == 'update':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
