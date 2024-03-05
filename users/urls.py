from django.urls import path, include
from .views import UserProfileView, UserProfileListView, UserProfileDetailView, FollowView, CreateUserView, FollowStatusView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/', UserProfileListView.as_view(), name='user-profile-list'),
    path('profiles/<str:username>/', UserProfileDetailView.as_view(),
         name='user-profile-detail'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow-user'),
    path('follow-status/<str:username>/',
         FollowStatusView.as_view(), name='follow-status'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
