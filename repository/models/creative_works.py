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
from common.utils import truncatelines

from things import CreativeWork, CreativeWorkManager, Person

# Create your models here.

class PoetryManager(CreativeWorkManager):
    '''
    @summary: The default manager for `Book` and `Article` class
    '''
    
    def apply_filter(self, *args, **kwargs):
        q_objects = Q()
        
        if 'language' in kwargs:
            q_objects &= Q(language=kwargs['language'])           
        
        return super(PoetryManager, self).apply_filter(*args, **kwargs).filter(q_objects)

    
class ArticleManager(CreativeWorkManager):
    '''
    @summary: The default manager for Article class
    '''
    
    def apply_filter(self, *args, **kwargs):        
        q_objects = Q()
        
        if 'language' in kwargs:
            q_objects &= Q(language=kwargs['language']) 
        if 'contributors' in kwargs:
            print contributors
            q_objects &= Q(contributors__in=kwargs['contributors'])            
        
        return super(ArticleManager, self).apply_filter(*args, **kwargs).filter(q_objects)    

    
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
    
    contributors = models.ManyToManyField(Person,
                                         related_name="%(class)s_contributed",
                                         blank=True,
                                         help_text=_('Secondary contributors to the creative work.')
                                         )    
    
    objects = ArticleManager()    
    
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
    
    # file will be saved to MEDIA_ROOT/uploads/2015/01/
    media = models.FileField(upload_to='repository/uploads/%Y/%m/',
                             null=True, blank=True,
                             help_text=_('A media for this creative work.')
                             )
    
    contributors = models.ManyToManyField(Person,
                                         related_name="%(class)s_contributed",
                                         blank=True,
                                         help_text=_('Secondary contributors to the creative work.')
                                         )
      
    objects = ArticleManager()
    
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
               
 
class Poetry(CreativeWork):
    '''
    @summary: A poetic article.
    @note:     
    '''
    
    language = models.CharField(max_length=8, 
                                choices=LANGUAGES, default='en',
                                help_text=_('The language of the content.')
                                )
        
    body = models.TextField(null=False,
                            help_text=_('The actual body of the article.')
                            )
    
    objects = PoetryManager()
        
    class Meta:
        verbose_name = _("Poetry")
        verbose_name_plural = _("Poetries")  

    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(LANGUAGES)
        return tmp[self.language]

    def summary(self):
        """
        Content to share on social media sites
        e.g. first stanza
        """
        return truncatelines(self.body, 4)

    def meta_description(self):
        return self.name + ' | poetry by ' + self.creator.name
