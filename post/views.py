from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from offer.permissions import IsObjectOwnerOrAdmin
from post.models import Post
from post.serializers import PostSerializer


class PostViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=['post'], detail=False, url_name='create', url_path=r'create')
    def create_post(self, request, **kwargs):
        serializer = PostSerializer(context={"request": request}, data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(owner=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False, url_name='delete', url_path=r'(?P<post_id>\d+)/delete')
    def delete_post(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        post.delete()
        return Response(data={'message': 'Pomyślnie usunięto'})

    @action(methods=['put'], detail=False, url_name='edit', url_path=r'edit/(?P<post_id>\d+)')
    def edit_post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, request.data, context={"request": request}, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(post, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_name='poast_all', url_path=r'all')
    def posts_list(self, request, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_name='detail', url_path=r'(?P<post_id>\d+)')
    def post_detail(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'poast_all':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete' or self.action == 'edit':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]