import re
from .main import ChatActions
from .models import Chat
from django.test import TestCase
from django.contrib.auth.models import User


class ChatTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test")

    def test_create_chat_without_user(self):
        c = ChatActions()
        chat_uuid = c.create()
        self.assertEqual(True, bool(re.match(r"([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})",
                                             str(chat_uuid))))
        self.assertEqual(1, Chat.objects.all().count())

    def test_create_chat_with_user(self):
        user = User.objects.get(username="test")
        c = ChatActions()
        chat_uuid = c.create(user)
        self.assertEqual(True, bool(re.match(r"([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})",
                                             str(chat_uuid))))
        self.assertEqual(1, Chat.objects.all().count())
        get_chat = Chat.objects.filter(uuid=chat_uuid).first()
        self.assertEqual('test', get_chat.user.username)

    def test_get_by_uuid(self):
        c = ChatActions()
        chat_uuid = c.create()
        get_chat = c.get_chat_by_uuid(chat_uuid)
        self.assertEqual(chat_uuid, get_chat.uuid)

    def test_get_by_user(self):
        user = User.objects.get(username="test")
        c = ChatActions()
        c.create(user)
        chats = c.get_chat_by_user(user)
        self.assertEqual(1, len(chats))

    def test_set_user_for_chat_by_uuid(self):
        user = User.objects.get(username="test")
        c = ChatActions()
        chat_uuid = c.create()
        chat = c.set_user_for_chat_by_uuid(chat_uuid, user)
        self.assertEqual(user, chat.user)

    def test_add_message(self):
        c = ChatActions()
        chat_uuid = c.create()
        get_chat = c.get_chat_by_uuid(chat_uuid)
        message = 'Hello world'
        add_message = c.add_message(get_chat, get_chat.user, message)
        self.assertEqual(message, add_message.message)

    def test_is_read(self):
        c = ChatActions()
        chat_uuid = c.create()
        get_chat = c.get_chat_by_uuid(chat_uuid)
        message = 'Hello world'
        add_message = c.add_message(get_chat, get_chat.user, message)
        is_read = c.mark_is_read(get_chat)
        add_message.refresh_from_db()
        self.assertEqual(True, is_read)
        self.assertEqual(True, add_message.is_read)

    def test_get_comment_list(self):
        c = ChatActions()
        chat_uuid = c.create()
        get_chat = c.get_chat_by_uuid(chat_uuid)
        message = 'Hello world'
        c.add_message(get_chat, get_chat.user, message)

        get_comment_list = c.get_comment_list(get_chat)
        self.assertEqual(1, len(get_comment_list))
        self.assertEqual(1, get_comment_list[0]['id'])
        self.assertEqual(message, get_comment_list[0]['message'])

        c.add_message(get_chat, get_chat.user, message)
        get_comment_list = c.get_comment_list(get_chat)
        self.assertEqual(2, len(get_comment_list))
        get_comment_list = c.get_comment_list(get_chat, 1)
        self.assertEqual(1, len(get_comment_list))
