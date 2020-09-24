from rest_framework import serializers
from comment.models import Comment
from user.serializer import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'offer', 'content', 'date']
        read_only_fields = ['owner']

    def create(self, validated_data):
        comment_data = validated_data.pop('content')
        offer_id = validated_data.pop('offer')
        comment = Comment.objects.create(content=comment_data, offer=offer_id, owner=self.context['request'].user)
        return comment
