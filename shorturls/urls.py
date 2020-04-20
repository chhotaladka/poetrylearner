from django.conf import settings
from django.conf.urls import include, url, patterns

app_name = 'shorturls'
urlpatterns = [
    
    url(
        regex = '^(?P<prefix>%s)(?P<tiny>\w+)$' % '|'.join(settings.SHORTEN_MODELS.keys()),
        view  = 'shorturls.views.redirect',
        name = 'redirect',
    ),
]