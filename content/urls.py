from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, StoryViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'stories', StoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
