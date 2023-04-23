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
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap

from repository.sitemaps import PersonSitemap, PoetrySitemap
from .sitemaps import StaticViewSitemap 
from . import views
from . import urls_allauth_blocked

sitemaps = {
    'static': StaticViewSitemap,
    'poet': PersonSitemap,
    'poetry': PoetrySitemap
}

app_name = 'core'

urlpatterns = [
    re_path(r'^$', views.welcome, name='welcome'),
    re_path(r'^about/?$', views.about, name='about'),
    re_path(r'^privacy/?$', views.privacy, name='privacy'),
    re_path(r'^accounts/', include('poetry.urls_allauth_blocked')),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^activity/', include('activity.urls', namespace='activity')),
    re_path(r'^bookmark/', include('bookmarks.urls', namespace='bookmark')),
    re_path(r'^c/', include('crawlers.urls', namespace='crawlers')),
    re_path(r'^feedback/', include('feedback.urls', namespace='feedback')),
    re_path(r'^r/', include('repository.urls', namespace='repository')),
    re_path(r'^u/', include('dashboard.urls', namespace='dashboard')),
    re_path(r'^proofreader/', include('proofreader.urls', namespace='proofreader')),
    
    re_path(r'^books/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.book, name='book'),
    re_path(r'^books/?$', views.explore_books, name='explore-books'),
    
    re_path(r'^poetry/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.poetry, name='poetry'),
    re_path(r'^poetry/?$', views.explore_poetry, name='explore-poetry'),
    
    re_path(r'^poets/(?P<pk>\d+)/(?P<slug>.+)?/books/?$', views.explore_books_of, name='explore-books-of'),
    re_path(r'^poets/(?P<pk>\d+)/(?P<slug>.+)?/poetry/?$', views.explore_poetry_of, name='explore-poetry-of'),
    re_path(r'^poets/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.poet, name='poet'),
    re_path(r'^poets/?$', views.explore_poets, name='explore-poets'),
    
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    
    re_path(r'^', include('shorturls.urls', namespace='shorturls')),
    
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
