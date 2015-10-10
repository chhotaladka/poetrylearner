from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode


class ActiveTagManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(ActiveTagManager, self).get_queryset().exclude(used_count__lt=1)

class Tag(models.Model):
    name            = models.CharField(max_length=255, unique=True)
    created_by      = models.ForeignKey(auth.models.User, related_name='created_tags')
    created_at      = models.DateTimeField(auto_now_add=True)
    # Denormalised data
    used_count = models.PositiveIntegerField(default=0)

    active = ActiveTagManager()

    class Meta:
        ordering = ('-used_count', 'name')
        app_label = 'snippets'

    def __unicode__(self):
        return force_unicode(self.name)

    def add_to_usage_count(self, value):
        if self.used_count + value < 0:
            self.used_count = 0
        else:
            self.used_count = models.F('used_count') + value

    @models.permalink
    def get_absolute_url(self):
        # TODO
        pass

