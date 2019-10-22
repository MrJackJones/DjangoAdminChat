import logging
from .models import Chat, ChatMessage
from django.utils import timezone
from django.contrib.auth.models import User

logger = logging.getLogger('main')


class ChatActions:
    def __init__(self):
        pass

    def create(self, user: User = None) -> str or None:
        try:
            chat = Chat.objects.create(user=user)
            return chat.uuid
        except Exception as e:
            logger.error(e)
            return

    def get_chat_by_uuid(self, uuid: str) -> Chat or None:
        try:
            chat = Chat.objects.filter(uuid=uuid).first()
            return chat
        except Exception as e:
            logger.error(e)
            return

    def get_chat_by_user(self, user: User) -> [Chat] or None:
        try:
            chats = Chat.objects.filter(user=user)
            if not chats:
                return

            return chats
        except Exception as e:
            logger.error(e)
            return

    def set_user_for_chat_by_uuid(self, uuid: str, user: User) -> Chat or None:
        try:
            chat = self.get_chat_by_uuid(uuid)
            if not chat:
                return
            chat.user = user
            chat.save()

            return chat
        except Exception as e:
            logger.error(e)
            return

    def add_message(self, chat: Chat, message: str = '') -> ChatMessage or None:
        try:
            comment = ChatMessage(
                chat=chat,
                user=chat.user,
                message=message,
            )
            comment.save()

            return comment
        except Exception as e:
            logger.error(e)
            return

    def mark_is_read(self, chat: Chat) -> bool or None:
        try:
            all_read_comments = chat.comment.filter(is_read=False)
            for comment in all_read_comments:
                comment.is_read = True
                comment.save()

            return True
        except Exception as e:
            logger.error(e)
            return

    def get_comment_list(self, chat: Chat, message_max: int or bool = False) -> list or None:
        try:
            comments = []

            all_comments = chat.comment.all().order_by('-id')
            if not all_comments:
                comments = []
            else:
                for comment in all_comments:
                    support_user = False
                    username = 'Unknown'
                    if comment.user:
                        if comment.user.is_superuser:
                            support_user = True
                        username = comment.user.username

                    comments.append({
                        'id': comment.pk,
                        'name': username,
                        'message': comment.message,
                        'from_admin': support_user,
                        'is_read': comment.is_read,
                        'created_at': timezone.localtime(comment.created_at).strftime('%d/%m/%Y %H:%M'),
                        'updated_at': timezone.localtime(comment.updated_at).strftime('%d/%m/%Y %H:%M'),
                    })

            if message_max:
                comments = comments[:message_max]

            return comments
        except Exception as e:
            logger.error(e)
            return
