from .models import Chat, ChatMessage
from django.utils import timezone
from django.contrib.auth.models import User


class ChatActions:
    def __init__(self):
        pass

    def create(self, user: User = None) -> str or None:
        """
        Create chat
        :param user: user: User or None
        :return: uuid: str or None
        """
        try:
            chat = Chat.objects.create(user=user)
            return chat.uuid
        except Exception:
            return

    def get_chat_by_uuid(self, uuid: str) -> Chat or None:
        """
        Get chat by UUID
        :param uuid: UUID: str
        :return: Chat or None
        """
        try:
            chat = Chat.objects.filter(uuid=uuid).first()
            return chat
        except Exception:
            return

    def get_chat_by_user(self, user: User) -> [Chat] or None:
        """
        Get chat by User
        :param user: user: User
        :return: list[Chat] or None
        """
        try:
            chats = Chat.objects.filter(user=user)
            if not chats:
                return

            return chats
        except Exception:
            return

    def set_user_for_chat_by_uuid(self, uuid: str, user: User) -> Chat or None:
        """
        Set user for chat by UUID
        :param uuid: UUID: str
        :param user: user: User
        :return: Chat or None
        """
        try:
            chat = self.get_chat_by_uuid(uuid)
            if not chat:
                return
            chat.user = user
            chat.save()

            return chat
        except Exception:
            return

    def add_message(self, chat: Chat, user: User, message: str = '') -> ChatMessage or None:
        """
        Add message
        :param chat: chat: Chat
        :param user: user: User
        :param message: message: str or ''
        :return: ChatMessage or None
        """
        try:
            comment = ChatMessage(
                chat=chat,
                user=user,
                message=message,
            )
            comment.save()

            return comment
        except Exception:
            return

    def mark_is_read(self, chat: Chat) -> bool or None:
        """
        Mark chat is_read
        :param chat: chat: Chat
        :return: bool or None
        """
        try:
            all_read_comments = chat.comment.filter(is_read=False)
            for comment in all_read_comments:
                comment.is_read = True
                comment.save()

            return True
        except Exception:
            return

    def get_comment_list(self, chat: Chat, message_max: int or bool = False) -> list or None:
        """
        Get comment list
        :param chat: chat: Chat
        :param message_max: message_max: int or bool = False
        :return: list or None
        """
        try:
            comments = []

            all_comments = chat.comment.all().order_by('id')
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
        except Exception:
            return
