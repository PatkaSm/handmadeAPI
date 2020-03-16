from django.http import JsonResponse
from django.shortcuts import render
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
        data = []
        for root in categories:
            data.append(CategorySerializer(root).data)
        return JsonResponse(data=data, status=200, safe=False)

    def get_permissions(self):
        if self.action == 'delete' or self.action == 'create' or self.action == 'update':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
