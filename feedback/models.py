from django.db import models
from django.contrib import auth
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Feedback(models.Model):
    '''
    @summary: Information about user's feedback about contents.
    '''

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
    content_object = generic.GenericForeignKey('content_type', 'object_id')


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
    
    def get_page_url(self):
        return self.url
    
    def get_content_url(self):
        if self.content_object:
            return self.content_object.get_absolute_url()
        return '#'

    def get_text(self):
        return self.text
    
    def get_action_taken(self):
        return self.action    
    