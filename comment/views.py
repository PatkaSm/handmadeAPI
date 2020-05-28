from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from comment.models import Comment
from comment.serializer import CommentSerializer
from offer.models import Offer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['post'], url_name='create', url_path='offer/(?P<offer_id>\d+)/create')
    def create_comment(self, request, **kwargs):
        comment = CommentSerializer(context={'request': request}, data=request.data)
        if not comment.is_valid():
            return Response(data=comment.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        comment.save(offer=offer, owner=request.user)
        return Response(data=comment.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='get_comments', url_path='offer/(?P<offer_id>\d+)')
    def get_comments(self, request, **kwargs):
        offer_comment = Comment.objects.filter(offer=kwargs.get('offer_id'))
        serializer = CommentSerializer(offer_comment, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)