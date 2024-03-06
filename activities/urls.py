from django.urls import path
from .views import CommentView, LikeToggleView

urlpatterns = [
    path('comments/<int:post_id>/', CommentView.as_view(), name='comment-create'),
    path('comments/delete/<int:comment_id>/',
         CommentView.as_view(), name='comment-delete'),
    path('likes/<int:post_id>/', LikeToggleView.as_view(), name='like-toggle'),
]
