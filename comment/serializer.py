from rest_framework import serializers

from comment.models import Comment
from user.serializer import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Comment
        fields = ['owner', 'offer', 'content', 'date']
        read_only_fields = ['owner', 'offer']

    def get_owner(self, instance):
        user = UserSerializer(instance=instance.owner,  context={'request': self.context['request']})
        return user.data
