from django.contrib import admin
from .models import Tag, Post, Story, Mention, Media

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'user', 'created_at']
    list_filter = ['created_at', 'tags']
    search_fields = ['caption', 'user__username']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'expires_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['user__username']

@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_object', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username']

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'media', 'media_type']
    list_filter = ['media_type']
    search_fields = ['post__caption']
