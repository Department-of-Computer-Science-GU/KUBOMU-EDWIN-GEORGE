# messaging/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']  # Prevent direct modification of sender and timestamp
