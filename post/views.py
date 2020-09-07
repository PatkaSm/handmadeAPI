from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from offer.permissions import IsObjectOwnerOrAdmin
from post.models import Post
from post.serializers import PostSerializer


class PostViewSet(mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, **kwargs):
        serializer = PostSerializer(context={"request": request}, data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(owner=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]
