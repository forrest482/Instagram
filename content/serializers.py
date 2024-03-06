from rest_framework import serializers
from .models import Post, Story, Tag, Media, Mention
from django.contrib.auth import get_user_model
from activities.models import Comment, Like

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        # Include 'profile_picture'
        fields = ['id', 'username', 'profile_picture']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            profile_picture_url = obj.profile.profile_picture.url
            return request.build_absolute_uri(profile_picture_url) if request else profile_picture_url
        return None  # Or a default image URL


class MentionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested UserSerializer

    class Meta:
        model = Mention
        # Include 'user' instead of just the user ID
        fields = ['id', 'user', 'timestamp']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    media = MediaSerializer(many=True, required=False)
    mentions = MentionSerializer(many=True, required=False)
    comments = CommentSerializer(
        many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'caption', 'user', 'created_at',
                  'tags', 'media', 'mentions', 'comments', 'likes']

    def create(self, validated_data):
        # Remove 'user' from validated_data if it exists
        validated_data.pop('user', None)

        # Get the user from the serializer context
        user = self.context['request'].user

        tags_data = validated_data.pop('tags', [])
        media_data = validated_data.pop('media', [])
        mentions_data = validated_data.pop('mentions', [])
        post = Post.objects.create(
            user=user, **validated_data)

        for tag_data in tags_data:
            Tag.objects.create(post=post, **tag_data)

        for media_datum in media_data:
            Media.objects.create(post=post, **media_datum)

        for mention_data in mentions_data:
            Mention.objects.create(post=post, **mention_data)

        return post


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
