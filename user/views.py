
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'], url_name='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['put'], url_name='update')
    def edit_user(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['get'], url_name='user_details')
    def user_details(self, request):
        serializer = UserSerializer(data=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


