from rest_framework import serializers

from chatApp.models import Message
from user.serializer import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']