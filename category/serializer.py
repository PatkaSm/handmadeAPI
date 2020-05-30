from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, instance):
        serializer = CategorySerializer(Category.objects.filter(parent=instance), many=True)
        return serializer.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children', 'img']
