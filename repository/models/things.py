from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q

from taggit.managers import TaggableManager

from base import Thing, ThingManager
from utils import Reference, TaggedItem, image_upload_path


# Create your models here.
class Organization(Thing):
    '''
    @summary: An organization such as a school, NGO, corporation, club, etc.
    @see: http://schema.org/Organization
    @note:
    
    '''

    ORGANIZATION_TYPE = (
        ('corp', 'Corporation'),
        ('edu', 'Educational Organization'),
        ('govt', 'Government Organization'),
        ('locl', 'Local Business'),
        ('ngo', 'NGO'),
        ('perf', 'Performing Group'),
        ('sport', 'Sports Organization'),
    )
    
    address = models.CharField(max_length=300,
                           null=True, blank=True,
                           help_text=_('Physical address of the item.')
                        )
    
    parent = models.ForeignKey('self',
                                on_delete=models.SET_NULL,
                                related_name="subsidiaries",
                                null=True, blank=True,
                                help_text=_('The larger organization that this organization is a branch of, if any.')
                            )
    
    type = models.CharField(max_length=8, 
                                choices=ORGANIZATION_TYPE, default='corp',
                                help_text=_('Type of the organization.')
                                )      

    def get_type(self):
        '''
        Returns the organization type
        '''
        tmp = dict(self.ORGANIZATION_TYPE)
        return tmp[self.type]
    
        
class Product(Thing):
    '''
    @summary: Any offered product or service. 
    For example: a pair of shoes; a concert ticket; the rental of a car; a haircut; or an episode of a TV show streamed online.
    @see: http://schema.org/Product
    @note:
    
    '''

    is_related_to = models.ManyToManyField('self',
                                         related_name="related_products",
                                         blank=True,
                                         help_text=_('A pointer to another, somehow related product (or multiple products).')
                                        ) 
    
    is_similar_to = models.ManyToManyField('self',                                         
                                         related_name="similar_products",
                                         blank=True,
                                         help_text=_('A pointer to another, functionally similar product (or multiple products).')
                                        )
    
    manufacturer = models.ForeignKey(Organization,
                                    on_delete=models.SET_NULL,
                                    related_name="owns",
                                    null=True, blank=True,
                                    help_text=_('The manufacturer of the product.')
                                )

    image = models.ImageField(upload_to=image_upload_path, 
                              null=True, blank=True,
                              help_text=_('An image of the item.')
                            )           
    
    def get_image_url(self):
        '''
        Return image url of the item. If not exist, return None.
        '''
        if self.image:
            return '{0}{1}'.format(settings.MEDIA_URL, self.image)            
        else:
            return None    
        
        
class Person(Thing):
    '''
    @summary: A person (alive, dead, undead, or fictional).
    @see: http://schema.org/Person
    @note:    
    
    '''
    
    GENDER_TYPE = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('o', 'Other'),
    )
        
    additional_name = models.CharField(max_length=200,
                               null=True, blank=True,
                               help_text=_('An additional name for a Person, can be used for a middle name.')
                            )
    
    affiliation = models.ManyToManyField(Organization,
                                         related_name="members",
                                         blank=True,
                                         help_text=_('Organization(s) that this person is affiliated with. For example, a school/university, a club, or a team.')
                                        )    
    
    year_birth = models.SmallIntegerField(_('year of birth'),
                                          null=True, blank=True,
                                          help_text=_('For years like 500 BC, use -500.')
                                          )
    
    year_death = models.SmallIntegerField(_('year of death'),
                                          null=True, blank=True,
                                          help_text=_('For years like 500 BC, use -500.')
                                          )
    
    gender = models.CharField(max_length=2, 
                              choices=GENDER_TYPE, default='m',
                              help_text=_('Gender of the person.')
                            ) 

    image = models.ImageField(upload_to=image_upload_path, 
                              null=True, blank=True,
                              help_text=_('An image of the item.')
                            ) 

    
    def get_image_url(self):
        '''
        Return image url of the item. If not exist, return None.
        '''
        if self.image:
            return '{0}{1}'.format(settings.MEDIA_URL, self.image)            
        else:
            return None

    def meta_description(self):
        p = 'his' if self.gender == 'm' else 'her'
        return self.name + ' and ' + p + ' poetry.'

    def clean(self):
        print "DBG:: Model Person clean called"
        # year_death must be greater than year_birth
        if self.year_birth is not None and self.year_death is not None:
            if self.year_death <= self.year_birth:
                raise ValidationError({
                    'year_death': "Foeticide is illegal. Death shouldn't happen before birth."
                })
                        
    def save(self, *args, **kwargs):                
        super(self.__class__, self).save(*args, **kwargs)
        print "DBG:: Model Person save called"        


class Place(Thing):
    '''
    @summary: Entities that have a somewhat fixed, physical extension.
    @see: http://schema.org/Place
    @note:
     
    '''
    
    address = models.CharField(max_length=300,
                           null=True, blank=True,
                           help_text=_('Physical address of the item.')
                        )
       
    has_map = models.URLField(null=True, blank=True,
                              help_text=_('A URL to a map of the place.')
                            )




class Event(Thing):
    '''
    @summary: An event happening at a certain time and location, such as a concert, lecture, or festival. 
    Repeated events may be structured as separate Event objects.
    @see: http://schema.org/Event
    @note:
    
    '''
    
    location = models.ForeignKey(Place,
                            on_delete=models.SET_NULL,
                            related_name="events",
                            null=True, blank=True,
                            help_text=_('The location of for example where the event is happening, or where an action takes place.')
                            )
    
    start_date = models.DateField(null=True, blank=True,
                                  help_text=_('The start date "YYYY-MM-DD" of the event.')
                                )
    
    end_date = models.DateField(null=True, blank=True,
                                  help_text=_('The end date "YYYY-MM-DD" of the event.')
                                )
    
    super_event = models.ForeignKey('self',
                                    on_delete=models.SET_NULL,
                                    related_name="sub_events",
                                    null=True, blank=True,
                                    help_text=_('An event that this event is a part of. e.g. a collection of individual music performances might each have a music festival as their super event.')
                                    )

    image = models.ImageField(upload_to=image_upload_path, 
                              null=True, blank=True,
                              help_text=_('An image of the item.')
                            )      

    def get_image_url(self):
        '''
        Return image url of the item. If not exist, return None.
        '''
        if self.image:
            return '{0}{1}'.format(settings.MEDIA_URL, self.image)            
        else:
            return None
        

class CreativeWorkManager(ThingManager):
    '''
    @summary: The default manager for CreativeWork class
    '''
    
    def apply_filter(self, *args, **kwargs):        
        q_objects = Q()
        
        if 'creator' in kwargs:
            q_objects &= Q(creator__id=kwargs['creator'])
        if 'publisher' in kwargs:
            print publisher
            q_objects &= Q(publisher__id=kwargs['publisher'])
            
        if 'published' in kwargs:
            if kwargs['published'] is True:
                # published items
                q_objects &= Q(date_published__isnull=False)
            else:
                # unpublished items
                q_objects &= Q(date_published__isnull=True)                        
        
        return super(CreativeWorkManager, self).apply_filter(*args, **kwargs).filter(q_objects)

    
class PublishedManager(models.Manager):
    '''
    @summary: Returns Published `CreativeWork`s
    '''    
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(date_published__isnull=False)    
    

class CreativeWork(Thing):
    '''
    @summary: The most generic kind of creative work, including books, movies, photographs, software programs, etc.
    @see: http://schema.org/CreativeWork
    @note: 

    '''
    
    creator = models.ForeignKey(Person,
                                on_delete=models.SET_NULL,
                                related_name="%(class)s_created",
                                null=True, blank=True,
                                help_text=_('The creator/author of this content.')
                                )
    
    date_published = models.DateTimeField(null=True, blank=True,
                                          help_text=_('Date of first broadcast/publication.')
                                        )    
    
    keywords = TaggableManager(blank=True,
                               through=TaggedItem,
                               help_text=_('Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas.')
                            )
    
    license = models.CharField(max_length=300,
                               null=True, blank=True,
                               help_text=_('A license document that applies to this content, typically indicated by URL.')
                               )
    
    publisher = models.ForeignKey(Organization,
                                  on_delete=models.SET_NULL,
                                  related_name="%(class)s_published",
                                  null=True, blank=True,
                                  help_text=_('The publisher(Person or Organization) of the creative work.')
                                  )
    
    objects = CreativeWorkManager()
    
    published = PublishedManager()
        
    class Meta:
        abstract = True
    
    def get_author(self):
        return self.creator
    
    def get_keywords(self):
        return self.keywords.names()
        
    def get_tags_names(self):
        return self.keywords.names()
    
    def get_tags_slugs(self):
        return self.keywords.slugs()
    
    def is_published(self):
        return True if self.date_published else False
    
    def get_media_url(self):
        '''
        Return media url of the item. If not exist, return None.
        '''
        if self.media:
            return '{0}{1}'.format(settings.MEDIA_URL, self.media)            
        else:
            return None        

