from django.db import models
from category.models import Category


class Item(models.Model):
    class Colors(models.TextChoices):
        RED = 'red', 'Czerwony'
        BLACK = 'black', 'Czarny'
        WHITE = 'white', 'Biały'
        BLUE = 'blue', 'Niebieski'
        YELLOW = 'yellow', 'Żółty'
        PINK = 'pink', 'Różowy'
        GREEN = 'green', 'Zielony'
        BROWN = 'brown', 'Brązowy'
        PURPLE = 'purple', 'Fioletowy'
        MULTICOLOUR = 'multicolour', 'Wielokolorowy'
        GOLD = 'gold', 'Złoty'
        SILVER = 'silver', 'Srebrny'

    class Days(models.TextChoices):
        NOW = 'now', '1-3 dni'
        WEEK = 'week', 'do 7 dni'
        MONTH = 'month', 'do 30 dni'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, choices=Colors.choices)
    ready_in = models.CharField(choices=Days.choices, max_length=255)

    def __str__(self):
        return str(self.name)
