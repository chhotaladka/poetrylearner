from django.conf import settings
from django.urls import re_path
from . import views

app_name = 'shorturls'
urlpatterns = [
    
    re_path(
        r'^(?P<prefix>%s)(?P<tiny>\w+)$' % '|'.join(settings.SHORTEN_MODELS.keys()),
        views.redirect,
        name = 'redirect',
    ),
]
