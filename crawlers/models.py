from django.db import models
from datetime import datetime
from django.contrib import auth
from django.core.urlresolvers import reverse
import json
from snippets.models.snippet import Snippet

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
    
    def withsnippet(self):
        qs = self.get_queryset().exclude(snippet=None)
        return qs        
 
    def withoutsnippet(self):
        qs = self.get_queryset().filter(snippet=None)
        return qs    
    
       
#
# Crawled articles from accros the web by web spiders (scrapy)
#
class RawArticle(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000)
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=False)
    added_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False)
    snippet = models.ForeignKey(Snippet, related_name='ref_articles', null=True, blank=True, verbose_name="related entry in article table")
    
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
    
    def get_source_url(self):
        return self.source_url
    
    def get_validity(self):
        return self.valid
           
    def get_title(self):               
        return self.title
    
    def get_author(self):        
        return self.author
    
    def get_poem(self):        
        return self.content
    
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
                       
#
# Crawled authors from accros the web by web spiders (scrapy)
#
class RawAuthor(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000)
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