from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from offer.permissions import IsAdmin, IsObjectOwnerOrAdmin
from user.models import User
from user.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_name='my_profile', url_path='me')
    def my_profile(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_name='disabled_user', url_path='user/disabled/(?P<user_id>\d+)')
    def disabled_user(self, request, **kwargs):
        disabled_user = get_object_or_404(User, id=kwargs.get('user_id'))
        disabled_user.active = False
        return Response(data={'success': 'Pomyślnie dezaktywowano użytkownika'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='search', url_path='search')
    def search(self, request):
        word = request.GET.get('search')
        results = User.objects.filter(nickname__contains=word).union(User.objects.filter(email__contains=word))
        serializer = UserSerializer(results, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve' or self.action == 'search':
            self.permission_classes = [AllowAny]
        if self.action == 'partial_update' or self.action == 'my_profile':
            self.permission_classes = [IsAuthenticated, IsObjectOwnerOrAdmin]
        if self.action == 'disabled_user' or self.action == 'destroy':
            self.permission_classes = [IsAdmin]

        return [permission() for permission in self.permission_classes]
