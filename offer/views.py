from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from offer.models import Offer
from offer.serializer import OfferSerializer


class OfferViewSet(viewsets.GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'], url_name='create_offer')
    def create_offer(self, request):
        serializer = OfferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([AllowAny])
    @action(detail=False, methods=['update'], url_name='edit_offer')
    def edit_offer(self, request):
        serializer = OfferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

