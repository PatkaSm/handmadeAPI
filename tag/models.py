from django.db import models


class Tag(models.Model):
    word = models.CharField(max_length=255)

    def __str__(self):
        return str(self.word)
