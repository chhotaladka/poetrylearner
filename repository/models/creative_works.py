from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags
from django.db.models import Q

from things import CreativeWork, CreativeWorkManager

# Create your models here.

class LiteratureManager(CreativeWorkManager):
    '''
    @summary: The default manager for `Book` and `Article` class
    '''
    
    def apply_filter(self, *args, **kwargs):
        q_objects = Q()
        
        if 'language' in kwargs:
            q_objects &= Q(language=kwargs['language'])           
        
        return super(LiteratureManager, self).apply_filter(*args, **kwargs).filter(q_objects)
    
    
    
class Book(CreativeWork):
    '''
    @summary: A book.
    @see: http://schema.org/Book
    @note: 
    
    '''

    language = models.CharField(max_length=8, 
                                choices=LANGUAGES, default='en',
                                help_text=_('The language of the book.')
                                )
        
    isbn = models.CharField(max_length=32,
                           null=True, blank=True,
                           help_text=_('The ISBN of the book.')
                        )
    
    objects = LiteratureManager()    
    
    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(LANGUAGES)
        return tmp[self.language]    
    

class Article(CreativeWork):
    '''
    @summary: An article, such as a news article or piece of investigative report.
    Newspapers and magazines have articles of many different types and this is intended to cover them all.
    @see: http://schema.org/Article
    @note: 
    
    '''

    language = models.CharField(max_length=8, 
                                choices=LANGUAGES, default='en',
                                help_text=_('The language of the content.')
                                )
        
    body = models.TextField(null=False,
                            help_text=_('The actual body of the article.')
                            )
    
    objects = LiteratureManager()
    
    class Meta:
        abstract = True        
                
    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(LANGUAGES)
        return tmp[self.language]
    
    def summary(self):
        if self.description:
            return self.description
        else:
            return strip_tags(self.body)[:200] + '...'          
               
        