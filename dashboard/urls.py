from django.urls import re_path

from . import views

app_name = 'dashboard'
urlpatterns = [

    re_path(r'^$', views.private_profile, name='private-profile'),
    re_path(r'^(?P<user_id>\d+)/(?P<slug>[^/]*)/?$', views.public_profile, name='public-profile'),
]
