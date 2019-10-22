# Django Admin Chat

Add chat to django

## Quick start

1. Add "chat" to INSTALLED_APPS:
```djangourlpath
  INSTALLED_APPS = {
    ...
    'chat'
  }
```

2. Include the chat URLconf in urls.py:

```djangourlpath
  path('', include('chat.urls'))
```
  

3. Run

```djangotemplate
  python manage.py makemigrations
  python manage.py migrate
```

4. Run the development server and access http://127.0.0.1:8000/admin/chat/ to manage chats.
