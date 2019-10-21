from django.contrib import admin
from django.conf.urls import url
from django.core.cache import cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect

from .models import Chat, ChatMessage


class ChatAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'last_comment']
    list_filter = ['user']
    readonly_fields = ('uuid', 'created_at', 'updated_at',)

    change_list_template = "admin/chat_changelist.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        response.context_data['users'] = User.objects.filter(is_active=True)

        return response

    def get_urls(self):
        urls = super(ChatAdmin, self).get_urls()
        my_urls = [
            url(r'^create', self.create_chat),
            url(r'^add_comment/(?P<pk>[0-9]+)$', self.add_comment),
            url(r'^update_data/(?P<pk>[0-9]+)$', self.update_data),
        ]
        return my_urls + urls

    def create_chat(self, request):
        user = request.POST['get_user']
        Chat.objects.create(user_id=user)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect(".")

    @csrf_exempt
    def update_data(self, request, pk):
        last_count_comment = cache.get('id:{}'.format(pk)) or 0
        chat = Chat.objects.filter(pk=pk).first()
        if not chat:
            return JsonResponse({
                'status': False,
            }, status=403)

        if last_count_comment >= chat.comment.count():
            return JsonResponse({
                'status': False,
            }, status=200)

        result = []

        cache.set('id:{}'.format(pk), chat.comment.count(), 360)

        for comment in chat.comment.all():
            data = {}
            if comment.user:
                if comment.user.is_superuser:
                    data['is_supper'] = True
            else:
                data['is_supper'] = False
            data['message'] = comment.message
            data['status'] = False
            data['is_read'] = comment.is_read
            data['created_at'] = comment.created_at.strftime("%D %H:%M:%S")
            data['name'] = comment.user.username if comment.user else ''
            result.append(data)

        return JsonResponse({
            'status': True,
            'data': result,
        }, status=200)

    @csrf_exempt
    def add_comment(self, request, pk):
        msg = request.POST.get('message')
        comment_id = request.POST.get('comment_id')

        if not msg:
            return JsonResponse({
                'status': False,
                'data': 'no_message',
            }, status=403)

        chat = Chat.objects.filter(pk=pk).first()
        if not chat:
            return JsonResponse({
                'status': False,
                'data': 'no_ticket',
            }, status=403)

        if comment_id:
            comment = request.user.comment_author.filter(pk=comment_id).first()  # type: ChatMessage
            if not comment:
                return JsonResponse({
                    'status': False,
                }, status=403)

            comment.message = msg

            comment.save()

            return JsonResponse({
                'status': True,
            }, status=200)

        comment = ChatMessage(
            user=request.user,
            chat=chat,
            message=msg,
        )

        comment.save()

        return JsonResponse({
            'status': True,
        }, status=200)

    def last_comment(self, obj):
        return render_to_string('admin/chat.html', context={
            'obj': obj,
        })

    last_comment.short_description = 'Messages'

    class Media:
        css = {
            'all': ('admin/css/chat.css',)
        }
        js = (
            'admin/js/chat.js',
        )

    def has_add_permission(self, request):
        return False


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Chat, ChatAdmin)
