from django.db import models
from django.urls import reverse
#from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from django.db.models import Q
import random
from common.utils import truncatelines

from .things import CreativeWork, CreativeWorkManager, Person
from repository.const import REPOSITORY_LANGUAGES

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
    
    def random(self, count=20, published=True):
        '''
        Random Poetry.
        '''
        q_objects = Q()
        if published:
            # published items
            q_objects &= Q(date_published__isnull=False)
        else:
            # unpublished items
            q_objects &= Q(date_published__isnull=True)
            
        q_ids = self.filter(q_objects).values_list('id', flat=True)
        id_list = list(q_ids)
        mix_ids = random.sample(id_list, min(count, len(id_list)))
        return super(PoetryManager, self).get_queryset().filter(pk__in=mix_ids)

    
class ArticleManager(CreativeWorkManager):
    '''
    @summary: The default manager for Article class
    '''
    
    def apply_filter(self, *args, **kwargs):        
        q_objects = Q()
        
        if 'language' in kwargs:
            q_objects &= Q(language=kwargs['language']) 
        if 'contributors' in kwargs:
            q_objects &= Q(contributors__in=kwargs['contributors'])            
        
        return super(ArticleManager, self).apply_filter(*args, **kwargs).filter(q_objects)    

    
class Book(CreativeWork):
    '''
    @summary: A book.
    @see: http://schema.org/Book
    @note: 
    
    '''

    language = models.CharField(max_length=8, 
                                choices=REPOSITORY_LANGUAGES, default='hi',
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
    
    def get_absolute_url(self):
        # Overriding the base method
        kwargs = {'pk': self.id, 'slug': self.get_slug(),}
        return reverse('book', kwargs=kwargs)
    
    def get_list_url(self):
        # Overriding the base method
        return reverse('explore-books')
    
    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(REPOSITORY_LANGUAGES)
        return tmp[self.language]
    

class Article(CreativeWork):
    '''
    @summary: An article, such as a news article or piece of investigative report.
    Newspapers and magazines have articles of many different types and this is intended to cover them all.
    @see: http://schema.org/Article
    @note: 
    
    '''

    language = models.CharField(max_length=8, 
                                choices=REPOSITORY_LANGUAGES, default='hi',
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
        tmp = dict(REPOSITORY_LANGUAGES)
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
                                choices=REPOSITORY_LANGUAGES, default='hi',
                                help_text=_('The language of the content.')
                                )
        
    body = models.TextField(null=False,
                            help_text=_('The actual body of the article.')
                            )
    
    objects = PoetryManager()
        
    class Meta:
        verbose_name = _("Poetry")
        verbose_name_plural = _("Poetry")

    def get_absolute_url(self):
        # Overriding the base method
        kwargs = {'pk': self.id, 'slug': self.get_slug(),}
        return reverse('poetry', kwargs=kwargs)
    
    def get_list_url(self):
        # Overriding the base method
        return reverse('explore-poetry')
    
    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(REPOSITORY_LANGUAGES)
        return tmp[self.language]

    def summary(self):
        """
        first stanza
        """
        return truncatelines(self.body, 4)
    
    def summary_socialmedia(self):
        """
        Content to share on social media sites.
        e.g. first two lines of first stanza
        """
        return truncatelines(self.body, 2, '%0A')

    def meta_description(self):
        return self.name + ' - poetry by ' + self.creator.name
