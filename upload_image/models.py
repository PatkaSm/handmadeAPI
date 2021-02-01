from django.db import models

def upload_location(instance, filename):
    return "item ID %s/%s" % (instance.id, filename)


class Image(models.Model):
    img = models.ImageField(null=True, blank=True, max_length=None, upload_to=upload_location)

