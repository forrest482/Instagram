from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    caption = models.TextField(blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    mentions = GenericRelation('Mention')

    def __str__(self):
        if self.caption:
            return f"Post by {self.user.username}: {self.caption[:50]}..."
        else:
            return f"Post by {self.user.username} (No Caption)"


class Story(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='stories/media/')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    tags = models.ManyToManyField(Tag, related_name='stories', blank=True)
    mentions = GenericRelation('Mention')

    def __str__(self):
        return f"{self.user.username}'s Story at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Mention(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentions')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} mentioned in {self.content_object}"


class Media(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='media')
    media = models.FileField(upload_to='posts/media/')
    media_type = models.CharField(max_length=10, choices=(
        ('image', 'Image'), ('video', 'Video')))

    def __str__(self):
        return f"{self.post.title} - {self.media_type}"
