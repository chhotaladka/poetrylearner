from django.conf.urls import include, url, patterns

from . import views

app_name = 'dashboard'
urlpatterns = [

    url(r'^$', views.private_profile, name='private-profile'),
    url(r'^(?P<user_id>\d+)/(?P<slug>[^/]*)/?$', views.public_profile, name='public-profile'),
]