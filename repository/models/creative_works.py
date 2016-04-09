from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags

from things import CreativeWork

# Create your models here.

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
               
        