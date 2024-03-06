from rest_framework import serializers
from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'post']

    def create(self, validated_data):
        # Remove 'user' from validated_data to avoid the "multiple values" error
        # Safely remove 'user' if it exists in validated_data
        validated_data.pop('user', None)

        # Access 'user' and 'post' from the context
        user = self.context['request'].user
        post = self.context['post']

        # Now create the Comment instance without passing 'user' twice
        return Comment.objects.create(user=user, post=post, **validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']
        read_only_fields = ['user', 'post']
