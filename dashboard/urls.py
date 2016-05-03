from django.conf.urls import include, url, patterns

from . import views


urlpatterns = [

    url(r'^(?P<user_id>\d+)?/?$', views.user_home, name='user-home'),
    url(r'^(?P<user_id>\d+)/profile/?$', views.user_profile, name='user-profile'),
    url(r'^(?P<user_id>\d+)/bookmarks/?$', views.user_bookmarks, name='user-bookmarks'),
    url(r'^(?P<user_id>\d+)/fav/?$', views.user_favorites, name='user-favorites'),
]