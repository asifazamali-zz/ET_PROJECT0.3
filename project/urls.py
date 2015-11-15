"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    url(r'^$','security.views.quiz',name='home'),
    url(r'^edit/','security.views.edit',name='edit'),
    url(r'^delete/','security.views.delete',name='delete'),
    url(r'^publish/','security.views.publish',name='publish'),
    url(r'^republish/','security.views.republish',name='re_publish'),
    url(r'^delete_post/','security.views.deletepost',name='delete_post'),

    url(r'^chats/', include('chat.urls'),name='chats'),
    url(r'^register/complete/$','security.views.registration_complete',name='registration_complete'),   
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),

]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
