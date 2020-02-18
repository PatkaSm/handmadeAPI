from rest_framework import serializers

from favourites.models import Favourite


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['user', 'offer']
