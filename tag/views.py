from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.permissions import IsAdmin
from tag.models import Tag
from tag.serializer import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update'\
                or self.action == 'retrieve':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]