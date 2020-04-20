from django.db import models
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import default
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#from django.utils.text import slugify
from django.utils.http import urlquote  as django_urlquote
from django.utils.http import urlencode as django_urlencode
from urllib.parse import urlparse
import random
from common.slugify import slugify 

# Create your models here.

class ThingManager(models.Manager):
    '''
    @summary: The default manager for Thing base class
    '''
    
    def apply_filter(self, *args, **kwargs):
        '''
        Return empty queryset
        Some derived classes would override this function.
        '''
        return super(ThingManager, self).get_queryset().all()
    
    def random(self, count=20):
        '''
        Random objects queryset.
        Some derived classes would override this function to get
        more meaningfull object mix.
        '''
        id_list = self.all().values_list('id', flat=True)
        total = len(id_list)
        count = count if total > count else total
        mix_ids = random.sample(id_list, count)
        return super(ThingManager, self).get_queryset().filter(pk__in=mix_ids)


class Thing(models.Model):
    '''
    @summary: The most generic type of item.
    @see: http://schema.org/Thing
    @note: 
    
    @param url: [http://schema.org/url] 
            URL of the item. The child class must implement `get_absolute_url` method. 
    '''
    
    name = models.CharField(max_length=300,
                            help_text=_('The name/title/headline of the item.')
                        )    
    description = models.TextField(null=True, blank=True,
                                   help_text=_('A short description of the item.')
                                )
    
    same_as = models.URLField(_('Similar Item'),
                              max_length=2000,
                              null=True, blank=True,
                              help_text=_("URL of a reference Web page that unambiguously indicates the item's identity. \
                              For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.")
                            )

    added_by = models.ForeignKey(auth.models.User, 
                                 related_name="%(app_label)s_%(class)s_added")
    
    date_added = models.DateTimeField(auto_now_add=True,
                                      help_text=_("The date time on which the item was created or the item was added to a DataFeed.")
                                      )
    
    modified_by = models.ForeignKey(auth.models.User,
                                    related_name="%(app_label)s_%(class)s_modified")
    
    date_modified = models.DateTimeField(blank=True,
                                         help_text=_("The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.")
                                        )
    
    objects = ThingManager()
            
    class Meta:
        abstract = True
               
    def __str__(self):          # on Python 3
        return self.name
    
    def __unicode__(self):      # on Python 2
        return self.name

    @classmethod
    def item_type(cls):
        return cls.__name__.lower()
    
    def get_content_type(self):
        '''
        Returns ContentType object
        '''
        return ContentType.objects.get_for_model(self)
        
    def get_slug(self):
        return slugify(self.name)
             
    def get_absolute_url(self):        
        kwargs = {'pk': self.id, 'slug': self.get_slug(), 'item_type': self.item_type()}
        return reverse('repository:item', kwargs=kwargs)

    def get_edit_url(self):        
        kwargs = {'pk': self.id, 'item_type': self.item_type()}
        return reverse('repository:add-item', kwargs=kwargs)        
    
    def get_list_url(self):
        kwargs = {'item_type': self.item_type()}
        return reverse('repository:list', kwargs=kwargs)

    def headline(self):
        return self.name
    
    def title(self):
        return self.name
    
    def summary(self):
        return self.description
    
    def summary_socialmedia(self):
        return self.description

    def meta_description(self):
        '''
        Used for meta tags in templates for SEO.
        Some derived classes would override this function.
        '''
        return self.description
    
    def get_keywords(self):
        '''
        Some derived classes would override this function.
        '''
        return None 

    def get_author(self):
        '''
        Some derived classes would override this function.
        '''
        return None     
    
    def similar_item_url(self): 
        return self.same_as
    
    def similar_item_name(self):
        # Returns domain name from the `same_as` 
        return urlparse(self.same_as).netloc
    
    def get_first_edit_user(self):
        return self.added_by
    
    def get_first_edit_time(self):
        return self.date_added
        
    def get_last_edit_user(self):
        return self.modified_by
    
    def get_last_edit_time(self):
        return self.date_modified
                
    def get_similar_item(self):
        '''
        URL of a reference Web page that unambiguously indicates the item's identity. 
        e.g. the URL of the item's Wikipedia page, Freebase page, or official website.
        '''
        return self.same_as
                    
         
