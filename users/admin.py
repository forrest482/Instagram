from django.contrib import admin
from .models import UserProfile, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_private']
    list_filter = ['is_private']
    search_fields = ['user__username']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'followed', 'created_at']
    search_fields = ['follower__username', 'followed__username']
