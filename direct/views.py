# In direct/views.py
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # You can customize the saving process here, for example, setting the sender
        serializer.save(sender=self.request.user)
