from django.http import JsonResponse
from django.shortcuts import render
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

    @action(detail=False, methods=['post'], url_name='create', url_path='offer/(?P<offer_id>\d+)/create')
    def create_comment(self, request, **kwargs):
        comment = CommentSerializer(context={'request': request}, data=request.data)
        if not comment.is_valid():
            return Response(data=comment.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        offer = get_object_or_404(Offer, id=kwargs.get('offer_id'))
        comment.save(offer=offer, owner=request.user)
        return Response(data={'message': 'Pomyślnie dodano komentarz'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='get_comments', url_path='offer/(?P<offer_id>\d+)/comments')
    def get_comments(self, request, **kwargs):
        offer_comment = Comment.objects.filter(offer=kwargs.get('offer_id'))
        serializer = CommentSerializer(offer_comment, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='delete_comment', url_path='comment/(?P<comment_id>\d+)/delete')
    def delete_comment(self, request, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('comment_id'))
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(data={'message': 'Pomyślnie usunięto komentarz'})

    @action(methods=['put'], detail=False, url_name='comment_edit',
            url_path=r'comment/(?P<comment_id>\d+)/edit')
    def comment_edit(self, request, **kwargs):
        print(request.data)
        serializer = CommentSerializer(data=request.data, context={"host": request.get_host()}, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        comment = get_object_or_404(Comment, id=kwargs.get('comment_id'))
        print(comment)
        self.check_object_permissions(request, comment)
        serializer.update(comment, serializer.validated_data)
        return JsonResponse(data=serializer.data, status=200, safe=False)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete_comment' or self.action == 'edit_comment':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'get_comments':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]