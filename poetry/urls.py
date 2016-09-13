"""poetry URL Configuration

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
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^activity/', include('activity.urls', namespace='activity')),
    url(r'^bookmark/', include('bookmarks.urls', namespace='bookmark')),
    url(r'^c/', include('crawlers.urls', namespace='crawlers')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
    url(r'^r/', include('repository.urls', namespace='repository')),
    url(r'^u/', include('dashboard.urls', namespace='dashboard')),
    
    url(r'^poetry/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.poetry, name='poetry'),
    url(r'^poetry/?$', views.list_poetry, name='list-poetry'),
    url(r'^poets/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.poet, name='poet'),
    url(r'^poets/?$', views.list_poet, name='list-poet'),
    url(r'^', include('shorturls.urls', namespace='shorturls')),
    
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
