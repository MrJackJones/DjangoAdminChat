import uuid
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    user = models.ForeignKey(User, related_name='chat', null=True, blank=True, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        permissions = (("manage_chat", "Can manage chats"),)
        verbose_name = 'Chat'
        verbose_name_plural = 'Chat'


class ChatMessage(models.Model):
    class Meta:
        ordering = ['id']

    chat = models.ForeignKey(Chat, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_author', null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField('Message', blank=False, null=False)
    is_read = models.BooleanField('is_read', default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
