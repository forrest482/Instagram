from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    # Adjust the fields as per your Message model
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    # Add search capability based on room name and content
    search_fields = ('receiver', 'content')
    list_filter = ('timestamp',)  # Enable filtering by timestamp


admin.site.register(Message, MessageAdmin)
