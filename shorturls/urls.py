from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'shorturls'
urlpatterns = [
    
    url(
        r'^(?P<prefix>%s)(?P<tiny>\w+)$' % '|'.join(settings.SHORTEN_MODELS.keys()),
        views.redirect,
        name = 'redirect',
    ),
]