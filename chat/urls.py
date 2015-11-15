from django.conf.urls import patterns, include, url
from chat import views

urlpatterns = patterns('',
        url(r'^$', views.chat_room, name='chats'),
        url(r'^accounts/', include('registration.backends.simple.urls')),
        #url(r'^long_poll/(?P<chat_room_id>\d+)/$', views.longpoll_chat_room, name='longpoll_chat_room'),
)
