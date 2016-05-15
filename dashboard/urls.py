from django.conf.urls import include, url, patterns

from . import views


urlpatterns = [

    url(r'^$', views.user_home, name='user-home'),    
    url(r'^profile/?$', views.private_profile, name='private-profile'),
    url(r'^bookmarks/?$', views.user_bookmarks, name='user-bookmarks'),
    url(r'^fav/?$', views.user_favorites, name='user-favorites'),
    url(r'^(?P<user_id>\d+)/(?P<slug>[^/]*)/?$', views.public_profile, name='public-profile'),
]