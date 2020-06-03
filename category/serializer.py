from rest_framework import serializers

from category.models import Category


class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = ParentSerializer(read_only=True)

    def get_children(self, instance):
        serializer = CategorySerializer(Category.objects.filter(parent=instance), many=True)
        return serializer.data


    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']
        read_only_fields = ['parent']







