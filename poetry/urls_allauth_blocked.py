# Blocking urls of  django-allauth which we are not using
from django.urls import re_path
from django.views import defaults

urlpatterns = [

    re_path(r'^password/change/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^password/set/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^password/reset/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^password/reset/done/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^password/reset/key/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^password/reset/key/done/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^email/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    re_path(r'^confirm-email/*', defaults.permission_denied, {'exception': Exception('url blocked')}),

]
