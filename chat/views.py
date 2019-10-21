import json
from .models import Chat, ChatMessage
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def default(request):
    return JsonResponse({
        'error': 'access_deny'
    }, status=403)


@csrf_exempt
def chat(request):
    try:
        data = json.loads(request.body.decode())
        uuid = data['uuid']
        message_max = data.get('max') or False
        message = data.get('message') or False
        is_read = data.get('is_read') or False

        if message_max:
            message_max = int(message_max)

    except:
        return JsonResponse({
            'error': 'error_get_request',
        }, status=403)

    if uuid:
        try:
            chat = Chat.objects.filter(uuid=uuid).first()
        except:
            return JsonResponse({
                'error': 'chat_is_invalid',
            }, status=403)

        if not chat:
            return JsonResponse({
                'error': 'chat_not_found',
            }, status=403)

        if message:
            comment = ChatMessage(
                chat=chat,
                user=chat.user,
                message=message,
            )
            comment.save()

            comment.refresh_from_db()

            comment_data = {
                'id': comment.pk,
                'created_at': timezone.localtime(comment.created_at).strftime('%d/%m/%Y %H:%M'),
            }

            return JsonResponse({
                'data': comment_data,
            }, status=200)

        if is_read:
            all_read_comments = chat.comment.filter(is_read=False)
            for comment in all_read_comments:
                comment.is_read = True
                comment.save()

            return JsonResponse({
                'data': True,
            }, status=200)

        comments = []

        all_comments = chat.comment.filter(status=False).all().order_by('-id')
        if not all_comments:
            comments = []
        else:
            for comment in all_comments:
                comments.append({
                    'id': comment.pk,
                    'from': 'user' if not comment.user else 'support',
                    'message': comment.message,
                    'is_read': comment.is_read,
                    'created_at': timezone.localtime(comment.created_at).strftime('%d/%m/%Y %H:%M'),
                    'updated_at': timezone.localtime(comment.updated_at).strftime('%d/%m/%Y %H:%M'),
                })

        if message_max:
            comments = comments[:message_max]

        return JsonResponse({
            'data': comments,
        }, status=200)

    return JsonResponse({
        'error': 'error_uuid',
    }, status=403)
