from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from chat.models import Message, Thread
from chat.serializer import MessageSerializer, ThreadSerializer


class ChatViewSet(viewsets.GenericViewSet):
    queryset = Thread.objects.all()

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
