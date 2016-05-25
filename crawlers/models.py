from django.db import models
from datetime import datetime
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.conf.global_settings import LANGUAGES
from django.contrib.contenttypes.models import ContentType
import json
from urlparse import urlparse

# Create your models here.

class ArticleManager(models.Manager):

    def get_queryset(self):
        qs = super(ArticleManager, self).get_queryset()
        return qs
    
    def valid(self):
        qs = self.get_queryset()
        qs = qs.filter(valid=True)
        return qs
    
    def invalid(self):
        qs = self.get_queryset().filter(valid=False)
        return qs

    def source_url(self, url):
        '''
        Objects with `source_url`` = url
        '''
        objs = self.filter(source_url=url)
        return objs
    
    def get_languages_for_url(self, url):
        '''
        Returns the list of languages in which the contents of objects are available 
        for source_url = ``url``
        '''
        objs = self.filter(source_url=url)
        list = []
        for obj in objs:
            list.append(obj.language)
        
        return list
      
       
#
# Crawled articles from accros the web by web spiders (scrapy)
#
class RawArticle(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000, db_index=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=False)
    added_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False) # Valid true means, this article once has been added to `Repository`
    language = models.CharField(max_length=8, choices=LANGUAGES, default='en')
        
    objects = ArticleManager()
    
    class Meta:
        ordering = ['-added_at']
             

    def __str__(self):          # on Python 3
        return self.source_url
    
    def __unicode__(self):      # on Python 2
        return self.source_url
      
    def get_absolute_url(self):
        kwargs = {'pk': str(self.id)}
        return reverse('crawlers:article-details', kwargs=kwargs)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))    
    
    def get_source_url(self):
        return self.source_url
    
    def get_source_name(self):
        # Returns domain name from the `source_url` 
        return urlparse(self.source_url).netloc
    
    def get_validity(self):
        return self.valid
           
    def get_title(self):               
        return self.title
    
    def get_author(self):        
        return self.author
    
    def get_poem(self):        
        return self.content
    
    def get_language(self):
        '''
        Returns the language full name
        '''
        tmp = dict(LANGUAGES)
        return tmp[self.language]    
    
    def save(self, *args, **kwargs):
        print "Model RawArticle save called"
              
        super(RawArticle, self).save(*args, **kwargs)


class AuthorManager(models.Manager):

    def get_queryset(self):
        qs = super(AuthorManager, self).get_queryset()
        return qs
    
    def valid(self):
        qs = super(AuthorManager, self).get_queryset()
        qs = qs.filter(valid=True)
        return qs
    
    def invalid(self):
        qs = super(AuthorManager, self).get_queryset().filter(valid=False)
        return qs
    
    def nobirth(self):
        qs = super(AuthorManager, self).get_queryset().filter(birth=None)
        return qs
    
    def nodeath(self):
        qs = super(AuthorManager, self).get_queryset().filter(death=None)
        return qs        

    def nodate(self):
        qs = super(AuthorManager, self).get_queryset().filter(birth=None, death=None)
        return qs
    
    def source_url(self, url):
        '''
        Objects with `source_url`` = url
        '''
        objs = self.filter(source_url=url)
        return objs    
                       
#
# Crawled authors from accros the web by web spiders (scrapy)
#
class RawAuthor(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000, db_index=True)
    name = models.CharField(max_length=200)
    birth = models.CharField(max_length=100, null=True, blank=True)
    death = models.CharField(max_length=100, null=True, blank=True)    
    added_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False)
    
    objects = AuthorManager()
    
    class Meta:
        ordering = ['-added_at']
             
    def __str__(self):          # on Python 3
        return self.name
    
    def __unicode__(self):      # on Python 2
        return self.name
      
    def get_absolute_url(self):
        kwargs = {'pk': str(self.id)}
        return reverse('crawlers:author-details', kwargs=kwargs)
    
    def get_source_url(self):
        return self.source_url
    
    def get_source_name(self):
        # Returns domain name from the `source_url` 
        return urlparse(self.source_url).netloc
        
    def get_validity(self):
        return self.valid
           
    def get_name(self):    
        return self.name
    
    def get_birth_date(self):
        #self.birth_year = self.birth_year.split()[-1]
        return self.birth

    def get_death_date(self):
        return self.death
    
    def get_next(self):
        next_issue = RawAuthor.objects.filter(id__gt=self.id).order_by('id')[0:1]
        if next_issue:
            return next_issue[0]
        else:
            # end of the table reached. Return first entry
            return RawAuthor.objects.all().order_by('id')[0]

    def get_previous(self):
        prev_issue = RawAuthor.objects.filter(id__lt=self.id).order_by('-id')[0:1]
        if prev_issue:
            return prev_issue[0]
        else:
            # end of the table reached. Return last entry
            return RawAuthor.objects.all().order_by('-id')[0]
            
    def save(self, *args, **kwargs):
        print "Model RawAuthor save called"
              
        super(RawAuthor, self).save(*args, **kwargs)