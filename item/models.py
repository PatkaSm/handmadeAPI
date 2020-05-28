from django.db import models

from category.models import Category

COLORS={('Czerwony', 'Czerwony'), ('Czarny','Czarny'), ('Biały', 'Biały'), ('Niebieski', 'Niebieski'),
        ('Żółty', 'Żółty'), ('Różowy', 'Różowy'), ('Zielony', 'Zielony'), ('Brązowy', 'Brązowy'),
        ('Fioletowy', 'Fioletowy')}

DAYS = {('1', '1-3 dni'), ('2', 'do 7 dni'), ('3', 'do 30 dni')}


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, choices=COLORS)
    ready_in = models.CharField(choices=DAYS, max_length=255)
    shipping_abroad = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
