from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment
from comment.serializer import CommentSerializer
from core.permissions import IsObjectOwnerOrAdmin


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_name='get_comments', url_path='offer/(?P<offer_id>\d+)')
    def get_comments(self, request, **kwargs):
        offer_comment = Comment.objects.filter(offer=kwargs.get('offer_id')).order_by('-date')
        serializer = CommentSerializer(offer_comment, many=True, context={'request': request})
        paginator = LimitOffsetPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'get_comments':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]