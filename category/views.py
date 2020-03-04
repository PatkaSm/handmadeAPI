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
        data = []
        categories = list(Category.objects.filter(parent=None))
        for root_index, category in enumerate(categories):
            children = list(Category.objects.filter(parent=category))
            data.append({
                "name": category.name,
                "children": []
            })
            for child_index, child in enumerate(children):
                data[root_index]["children"].append({
                    "name": child.name,
                    "children": []
                })
                second_childrens = list(Category.objects.filter(parent=child))
                for second_child in second_childrens:
                    data[root_index]["children"][child_index]["children"].append({
                        "name": second_child.name
                    })
        return JsonResponse(data=data, status=200, safe=False)

    def get_permissions(self):
        if self.action == 'delete' or self.action == 'create' or self.action == 'update':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
