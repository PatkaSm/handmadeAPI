from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from chatApp.models import Message
from chatApp.serializer import MessageSerializer
from user.models import User


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'], url_name='message_list', url_path='message/(?P<receiver_id>\d+)')
    def message_list(self, request, **kwargs):
        messages = Message.objects.filter(sender_id=request.user, receiver_id=kwargs.get('receiver_id'))
        serializer = MessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=['post'], url_name='send_message', url_path='message')
    def send_message(self, request):
        data = JSONParser().parse(request)
        print(data)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_name='chat', url_path='chat/(?P<receiver_id>\d+)')
    def chat(self, request, receiver):
        sender = User.objects.filter(user=request.user)
        receivers = User.objects.get(id=receiver)
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(
            sender_id=receiver, receiver_id=sender)
        data = {
            'sender': sender,
            'receiver': receivers,
            'messages': messages
        }
        return JsonResponse(data=data)

    def get_permissions(self):
        if self.action == 'message_view' or self.action == 'message_list' or self.action == 'chat':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
