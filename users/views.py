from rest_framework import generics, status, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Follow
from .serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile


class FollowView(views.APIView):
    def post(self, request, username):
        try:
            to_follow = User.objects.get(username=username)
            follow, created = Follow.objects.get_or_create(
                follower=request.user, followed=to_follow)
            if created:
                return Response({'status': 'following'}, status=status.HTTP_201_CREATED)
            return Response({'status': 'already following'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username):
        try:
            to_unfollow = User.objects.get(username=username)
            Follow.objects.filter(follower=request.user,
                                  followed=to_unfollow).delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'status': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
