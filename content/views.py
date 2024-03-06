from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.models import Follow
from .models import Post, Story, Media, Tag, Mention
from .serializers import PostSerializer, StorySerializer
from django.contrib.contenttypes.models import ContentType
import mimetypes


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='following', permission_classes=[IsAuthenticated])
    def posts_from_following(self, request):
        following_user_ids = Follow.objects.filter(
            follower=request.user).values_list('followed_id', flat=True)
        posts = Post.objects.filter(user_id__in=following_user_ids).order_by('-created_at').prefetch_related(
            'comments',
            'likes'
        )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save post with the current user
            post = serializer.save()

            # Handle Media
            media_files = request.FILES.getlist('media')
            for media_file in media_files:
                # Determine media type based on file MIME type
                mime_type, _ = mimetypes.guess_type(media_file.name)
                if mime_type:
                    media_type = 'video' if mime_type.startswith(
                        'video/') else 'image'
                else:
                    media_type = 'unknown'  # Fallback media type

                Media.objects.create(
                    post=post, media=media_file, media_type=media_type)

            # Handle Tags
            # Assuming tag names are sent in the request
            tags_names = request.data.getlist('tags')
            for tag_name in tags_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            # Handle Mentions
            # Assuming usernames are sent in the request
            mention_usernames = request.data.getlist('mentions')
            for username in mention_usernames:
                mentioned_user = User.objects.get(username=username)
                Mention.objects.create(
                    user=mentioned_user,
                    content_object=post,
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
