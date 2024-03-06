from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Like
from .serializers import CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from content.models import Post


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={
                                       'request': request, 'post': post})
        if serializer.is_valid():
            serializer.save()  # 'user' and 'post' are already in the context
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id, user=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeToggleView(APIView):
    def post(self, request, post_id, format=None):  # Notice `post_id` is expected here
        try:
            post = Post.objects.get(pk=post_id)
            like_qs = Like.objects.filter(user=request.user, post=post)

            if like_qs.exists():
                like_qs.delete()
                return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
            else:
                Like.objects.create(user=request.user, post=post)
                return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
