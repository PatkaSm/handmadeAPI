from django.db import models
from itertools import chain


def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False )
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, max_length=None, upload_to=upload_location)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def check_if_have_children(self, category):
        categories = []
        category_children = category.children
        for cat in category_children:
            categories.append(cat)

    def subcategories(self):
        """For a given category, returns list of all descending categories"""
        subcategories = [child.subcategories() for child in self.children.all()]
        return [self, *chain(*subcategories)]
