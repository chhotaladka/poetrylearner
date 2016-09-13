from django.conf import settings
from django.conf.urls import include, url, patterns

urlpatterns = [
    
    url(
        regex = '^(?P<prefix>%s)(?P<tiny>\w+)$' % '|'.join(settings.SHORTEN_MODELS.keys()),
        view  = 'shorturls.views.redirect',
        name = 'redirect',
    ),
]