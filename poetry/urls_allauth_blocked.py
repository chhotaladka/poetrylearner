# Blocking urls of  django-allauth which we are not using
from django.conf.urls import url
from django.views import defaults

urlpatterns = [

    url(r'^password/change/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^password/set/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^password/reset/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^password/reset/done/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^password/reset/key/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^password/reset/key/done/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^email/$', defaults.permission_denied, {'exception': Exception('url blocked')}),
    url(r'^confirm-email/*', defaults.permission_denied, {'exception': Exception('url blocked')}),

]