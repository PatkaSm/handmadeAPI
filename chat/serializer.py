from rest_framework import serializers

from chat.models import Message, Thread
from user.serializer import UserSerializer


class ThreadSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(many=False, read_only=True)
    user2 = UserSerializer(many=False, read_only=True)
    last_message = serializers.SerializerMethodField('get_message', read_only=True)

    def get_message(self, instance):
        last_message = Message.objects.filter(thread=instance).order_by('date_send')
        if not last_message:
            return None
        return MessageSerializer(last_message[0]).data

    class Meta:
        model = Thread
        fields = ['id', 'user1', 'user2', 'last_message']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'content', 'date_send', 'sender']