from django.db import models

from offer.models import Offer
from user.models import User


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
