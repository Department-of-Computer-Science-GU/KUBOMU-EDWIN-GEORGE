# messaging/models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    content = models.TextField()  # This is where you define the message body
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.subject} from {self.sender} to {self.recipient}'
