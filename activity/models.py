from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.timesince import timesince as djtimesince
from django.contrib.contenttypes.models import ContentType

VERBS = {
    'ADDITION': u'added',
    'CHANGE': u'updated',
    'DELETION': u'deleted',
    'PUBLISH': u'published',
    'UNPUBLISH': u'unpublished',
}


class ActionManager(models.Manager):
    '''
    @summary: Default manager for ``Action``
    '''
    use_in_migrations = True

    def log_action(self,
                   timestamp,
                   user,
                   target_content_type,
                   target_object_id,
                   target_object_repr,
                   verb,
                   change_message,
                   public=True,
                ):
        e = self.model(
            timestamp = timestamp,
            actor = user,
            target_content_type = target_content_type,
            target_object_id = target_object_id,
            target_object_repr = target_object_repr[:200],
            verb = verb,
            change_message = change_message,
            public = bool(public),
        )
        if timestamp:
            e.timestamp = timestamp
        e.save()

    def public(self, *args, **kwargs):
        '''
        Only return public actions
        '''
        kwargs['public'] = True
        return self.filter(*args, **kwargs)
    
    def actor(self, user, **kwargs):
        '''
        Stream of most recent actions where user is the actor.
        Keyword arguments will be passed to Action.objects.filter
        '''
        return self.filter(actor=user, **kwargs)
    
    def target(self, obj, **kwargs):
        '''
        Stream of most recent actions where obj is the target.
        Keyword arguments will be passed to Action.objects.filter
        '''
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(target_content_type=content_type,
                           target_object_id = obj.id,
                           **kwargs)


class Action(models.Model):
    """
    @summary: Action model describing the actor acting out a verb (on an optional
    target).

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>

    Examples::

        <chhotaladka> <became editor> <1 minute ago>
        <chhotaladka> <updated> <Kabir Das> <2 hours ago>
        <chhotaladka> <added> <The Prophet> <8 minutes ago>

    Unicode Representation::

        chhotaladka became editor 1 minute ago
        chhotaladka added The Prophet 3 days ago

    """
    timestamp = models.DateTimeField(default=timezone.now,
                                     db_index=True)

    actor = models.ForeignKey(User,
                              related_name='actor',
                              db_index=True)

    target_content_type = models.ForeignKey(ContentType,
                                     blank=True, null=True,
                                     db_index=True)
    target_object_id = models.PositiveIntegerField(blank=True, null=True,
                                 db_index=True)
    target_object_repr = models.CharField(max_length=200,
                                          blank=True, null=True)

    verb = models.CharField(max_length=32)

    change_message = models.TextField(blank=True, null=True)

    public = models.BooleanField(default=True,
                                 db_index=True)

    objects = ActionManager()

    class Meta:
        ordering = ('-timestamp', )

    def __str__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.get_verb(),
            'target': self.target_object_repr,
            'timesince': self.timesince()
        }#FIXME error
        if self.target_object_id:
            return '%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
        return '%(actor)s %(verb)s %(timesince)s ago' % ctx

    def is_addition(self):
        return self.verb == VERBS['ADDITION']

    def is_change(self):
        return self.verb == VERBS['CHANGE']

    def is_deletion(self):
        return self.verb == VERBS['DELETION']
    
    def is_publish(self):
        return self.verb == VERBS['PUBLISH']
    
    def is_unpublish(self):
        return self.verb == VERBS['UNPUBLISH']
    
    def get_verb(self):
        return self.verb
    
    def actor_url(self):
        return self.actor.profile.get_absolute_url()

    def target_url(self):
        "Returns the target (i.e. edited object) represented by this Action"
        target = self.target_content_type.get_object_for_this_type(pk=self.target_object_id)
        return target.get_absolute_url()
    
    def target_name(self):
        return self.target_object_repr
    
    def timesince(self, now=None):
        '''
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        '''
        return djtimesince(self.timestamp, now).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')

    def log_addition(self, request, object):
        """
        Log that an object has been successfully added.

        The default implementation creates an admin Action object.
        """
        pass

    def log_change(self, request, object, message):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin Action object.
        """
        pass

    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.

        The default implementation creates an admin Action object.
        """
        pass
