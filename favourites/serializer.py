from rest_framework import serializers

from favourites.models import Favourite
from offer.serializer import OfferReadSerializer


class FavouriteSerializer(serializers.ModelSerializer):
    offer = serializers.SerializerMethodField()

    class Meta:
        model = Favourite
        fields = ['offer', 'user']

    def get_offer(self, obj):
        return OfferReadSerializer(obj.offer, context=self.context).data


