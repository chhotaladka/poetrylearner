from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.

FEEDBACK_RATING_MAX = +10
FEEDBACK_RATING_MIN = -10
FEEDBACK_RATING_DEFAULT = 0 

class Feedback(models.Model):
    '''
    @summary: Information about user's feedback about contents.
    '''
    
    RATING_OPTIONS = [(i, i) for i in range(FEEDBACK_RATING_MIN, FEEDBACK_RATING_MAX + 1)]
    
    url = models.URLField(max_length=2000,
                          help_text=_('Feedback URL.'),
                        )

    text = models.TextField(help_text=_('Feedback text.'),
                            blank=True,
                        )

    action = models.TextField(max_length=1000,
                            help_text=_('Action taken on the feedback.'),
                            null=True, blank=True,
                        )
    
    rating = models.IntegerField(choices=RATING_OPTIONS, default=FEEDBACK_RATING_DEFAULT,
                                 help_text=_('Rating given by user as feedback OR given by us on feedback.'),
                                 null=True, blank=True,
                                )
    
    date_responded = models.DateTimeField(null=True, blank=True,
                                          help_text=_('Date time of last response/action on the feedback.')
                                        )
        
    email = models.EmailField(help_text=_('Email field, if user isn\'t logged in and wants to send her email.'),
                              null=True, blank=True,
                            )
    
    added_by = models.ForeignKey(auth.models.User, 
                                 related_name="%(app_label)s_%(class)s_added",
                                 null=True, blank=True,
                                )
    
    date_added = models.DateTimeField(auto_now_add=True,
                                      help_text=_("The date time on which the item was created or the item was added to a DataFeed."),
                                    )

    # Generic Foreign Key to the object this feedback is about
    content_type = models.ForeignKey(ContentType,
                                     related_name='feedback_content_objects',
                                     null=True, blank=True,
                                    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        if self.added_by:
            return '{0} - {1}'.format(self.date_added, self.added_by)
        elif self.email:
            return '{0} - {1}'.format(self.date_added, self.email)
        
        return '{0}'.format(self.date_added)
    
    def get_user_email(self):
        if self.added_by:
            return self.added_by.email
        return self.email
    
    def get_user(self):
        if self.added_by:
            return self.added_by
        else:
            return None
    
    def get_page_url(self):
        return self.url
    
    def get_content_url(self):
        if self.content_object:
            return self.content_object.get_absolute_url()
        return '#'

    def get_text(self):
        return self.text
    
    def get_rating(self):
        return self.rating
    
    def is_responded(self):
        '''
        returns True if response/action has been updated to `action` field.
        '''
        if self.action:
            return True
        else:
            return False
    
    def get_action_taken(self):
        return self.action    
    
    def get_absolute_url(self):
        kwargs = {'pk': str(self.id)}
        return reverse('feedback:response', kwargs=kwargs)    
    