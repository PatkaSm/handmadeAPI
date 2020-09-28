from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment
from comment.serializer import CommentSerializer
from offer.models import Offer
from offer.permissions import IsObjectOwnerOrAdmin


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['get'], url_name='get_comments', url_path='offer/(?P<offer_id>\d+)')
    def get_comments(self, request, **kwargs):
        offer_comment = Comment.objects.filter(offer=kwargs.get('offer_id'))
        serializer = CommentSerializer(offer_comment, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'get_comments':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]