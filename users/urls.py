from django.urls import path, include
from .views import UserProfileView, FollowView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', FollowView.as_view(), name='unfollow-user'),

]
