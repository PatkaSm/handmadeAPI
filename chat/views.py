from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from chat.models import Message, Thread
from chat.serializer import MessageSerializer, ThreadSerializer
from user.models import User


class ChatViewSet(viewsets.GenericViewSet):
    queryset = Thread.objects.all()

    @action(detail=False, methods=['GET', 'POST'], url_name='messages', url_path=r'(?P<id>\d+)')
    def messages(self, request, **kwargs):
        user_2 = User.objects.get(id=kwargs.get('id'))
        try:
            thread = Thread.objects.get_or_create(request.user, user_2)
        except Thread.DoesNotExist:
            return Response(data={'message': 'Nie możesz czatować sam ze sobą!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = ThreadSerializer(thread)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_name='threads', url_path='threads_list')
    def threads_list(self, request, **kwargs):
        user_id = request.user.id
        threads = Thread.objects.filter(user1_id=user_id).union(Thread.objects.filter(user2_id=user_id))
        serializer = ThreadSerializer(threads, many=True, context={'request': request})
        paginator = PageNumberPagination()
        paginator.page_size = 10
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(detail=False, methods=['GET'], url_name='messages', url_path='messages')
    def messages_list(self, request, *args):
        thread_id = request.query_params.get('threadId')
        messages = Message.objects.filter(thread_id=thread_id).order_by('-date_send')
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        paginator = PageNumberPagination()
        paginator.page_size = 12
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)
