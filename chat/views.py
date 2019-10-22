import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .main import ChatActions


@csrf_exempt
def chat(request):
    try:
        data = json.loads(request.body.decode())
        uuid = data['uuid']
        message_max = data.get('max') or False
        message = data.get('message') or ''
        is_read = data.get('is_read') or False

        if message_max:
            message_max = int(message_max)

    except Exception:
        return JsonResponse({
            'error': 'error_get_request',
        }, status=403)

    if uuid:
        c = ChatActions()

        try:
            chat = c.get_chat_by_uuid(uuid=uuid)
        except Exception:
            return JsonResponse({
                'error': 'chat_is_invalid',
            }, status=403)

        if not chat:
            return JsonResponse({
                'error': 'chat_not_found',
            }, status=403)

        if message:
            comment = c.add_message(chat, chat.user, message)

            if not comment:
                return JsonResponse({
                    'error': 'error_add_comment',
                }, status=403)

            comment_data = {
                'id': comment.pk,
                'created_at': timezone.localtime(comment.created_at).strftime('%d/%m/%Y %H:%M'),
            }

            return JsonResponse({
                'data': comment_data,
            }, status=200)

        if is_read:
            if not c.mark_is_read(chat):
                return JsonResponse({
                    'error': 'error_mark_is_read',
                }, status=403)

            return JsonResponse({
                'data': True,
            }, status=200)

        comments = c.get_comment_list(chat, message_max)

        if not comments:
            return JsonResponse({
                'error': 'get_comment_list',
            }, status=403)

        return JsonResponse({
            'data': comments,
        }, status=200)

    return JsonResponse({
        'error': 'error_uuid',
    }, status=403)
