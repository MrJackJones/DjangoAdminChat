from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.conf.urls import url
from django.core.cache import cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .main import ChatActions
from .models import Chat


class DisableChatsWithoutCommentsFilter(SimpleListFilter):
    title = 'Don`t show chats without comments'
    parameter_name = 'disable'

    def lookups(self, request, model_admin):
        return (
            ('disable', 'Don`t show'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(~Q(comment__chat=None))
        return queryset


class ShowChatsWithNewUserCommentsFilter(SimpleListFilter):
    title = 'Show chats with new user comments'
    parameter_name = 'chat'

    def lookups(self, request, model_admin):
        return (
            ('show', 'Show'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(~Q(comment__user__is_superuser=True) &
                                   ~Q(comment__chat=None))
        return queryset


class ChatAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'messages']
    list_filter = ['user', DisableChatsWithoutCommentsFilter, ShowChatsWithNewUserCommentsFilter]
    search_fields = ['user__username', 'uuid']
    readonly_fields = ('uuid', 'created_at', 'updated_at',)

    change_list_template = "admin/chat_changelist.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            response.context_data['users'] = User.objects.filter(is_active=True)
        except (AttributeError, KeyError):
            return response

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
        c = ChatActions()

        user_id = request.POST['get_user']
        user = None

        if user_id:
            user = User.objects.get(id=user_id)

        chat_uuid = c.create(user)
        self.message_user(request, "Chat created with UUID: {}".format(chat_uuid))

        return HttpResponseRedirect(".")

    @csrf_exempt
    def update_data(self, request, pk):
        last_count_comment = cache.get('id:{}'.format(pk)) or 0
        chat = Chat.objects.filter(pk=pk).first()
        if not chat:
            return JsonResponse({
                'status': False,
            }, status=403)

        count = chat.comment.count()

        if last_count_comment >= count:
            return JsonResponse({
                'status': False,
            }, status=200)

        c = ChatActions()
        result = c.get_comment_list(chat)
        cache.set('id:{}'.format(pk), count, 360)

        return JsonResponse({
            'status': True,
            'data': result,
        }, status=200)

    @csrf_exempt
    def add_comment(self, request, pk):
        message = request.POST.get('message')

        if not message:
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

        c = ChatActions()
        c.add_message(chat, request.user, message)

        return JsonResponse({
            'status': True,
        }, status=200)

    def messages(self, obj):
        return render_to_string('admin/chat.html', context={
            'obj': obj,
        })

    messages.short_description = 'Messages'

    class Media:
        css = {
            'all': ('admin/css/chat.css',)
        }
        js = (
            'admin/js/chat.js',
        )

    def has_add_permission(self, request):
        return False


admin.site.register(Chat, ChatAdmin)
