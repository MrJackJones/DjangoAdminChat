from django.conf.urls import include
from django.urls import path
from .views import chat
from django.contrib import admin

urlpatterns = [
    path('api/v1/', include([
        path('chat', chat, name='chat'),
    ])),

]

admin.site.index_template = 'admin/index.html'
admin.autodiscover()
