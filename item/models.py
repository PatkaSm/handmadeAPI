from django.db import models

CATEGORIES = [("Clothes","Clothes"),("Decorations","Decorations"),("Food","Food"),("Furniture","Furniture"),("Toys","Toys"),
              ("Other", "Other")]


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES, default='Other')

    def __str__(self):
        return str(self.name)
