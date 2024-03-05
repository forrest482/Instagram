from rest_framework import generics, status, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Follow
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.select_related(
        'user').all()  # Optimize query performance
    serializer_class = UserProfileSerializer

    # Override the get_object method to perform the lookup by username
    def get_object(self):
        # Get the username from URL kwargs
        username = self.kwargs.get('username')
        # Lookup UserProfile by related User's username
        return UserProfile.objects.get(user__username=username)


class FollowView(views.APIView):
    permission_classes = [IsAuthenticated]

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


class FollowStatusView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            target_user = User.objects.get(username=username)
            is_following = Follow.objects.filter(
                follower=request.user, followed=target_user).exists()
            return Response({'is_following': is_following})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
