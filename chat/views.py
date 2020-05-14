from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from chat.models import Message
from chat.serializer import MessageSerializer
from user.models import User
from user.serializer import UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'], url_name='chat', url_path='chat/(?P<receiver_id>\d+)')
    def chat(self, request, **kwargs):
        sender_data = request.user
        sender = UserSerializer(sender_data, context={'request': request})
        receiver_data = User.objects.get(id=kwargs.get('receiver_id'))
        receiver = UserSerializer(receiver_data, context={'request': request})
        messages_data = (Message.objects.filter(sender=sender_data, receiver=receiver_data) | Message.objects.filter(
            sender=receiver_data, receiver=sender_data)).order_by('timestamp')
        messages = MessageSerializer(messages_data, many=True, context={'request': request})
        data = {
            'sender': sender.data,
            'receiver': receiver.data,
            'messages': messages.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_name='send_message', url_path='message')
    def send_message(self, request):
        serializer = MessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(receiver=User.objects.get(id=request.data['receiver']), sender=User.objects.get(id=request.data['sender']))
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)




