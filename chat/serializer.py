from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='nickname')
    receiver = serializers.SlugRelatedField(read_only=True, slug_field='nickname')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
        read_only_fields = ['sender', 'receiver']
