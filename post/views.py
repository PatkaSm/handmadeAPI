from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.permissions import IsObjectOwnerOrAdmin
from core.views import MultiSerializerMixin
from post.models import Post
from post.serializers import PostSerializer, PostReadSerializer


class PostViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    paginator = LimitOffsetPagination()

    serializers = {
        'create': PostSerializer,
        'update': PostSerializer,
        'partial_update': PostSerializer,
        'list': PostReadSerializer,
        'retrieve': PostReadSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve'\
                or self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]
