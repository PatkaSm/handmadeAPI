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
        print(validated_data)
        comment = Comment.objects.create(content=validated_data['content'], offer=validated_data['offer'],
                                         owner=self.context['request'].user)
        return comment
