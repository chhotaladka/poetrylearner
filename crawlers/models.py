from django.db import models
from datetime import datetime
from django.contrib import auth
from django.core.urlresolvers import reverse
import json
from snippets.models.snippet import Snippet

# Create your models here.

#
# Crawled articles from accros the web by web spiders (scrapy)
#
class RawArticle(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000)
    content = models.TextField(null=False)
    added_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False)
    snippet = models.ForeignKey(Snippet, related_name='ref_articles', null=True, blank=True, verbose_name="related entry in article table")
    
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
        # return title extracted from self.content
        return json.loads(self.content)['title']
    
    def get_author(self):
        # return author extracted from self.content
        return json.loads(self.content)['author']
    
    def get_poem(self):
        # return poem extracted from self.content
        return json.loads(self.content)['poem']
    
    def save(self, *args, **kwargs):
        print "Model RawArticle save called"
              
        super(RawArticle, self).save(*args, **kwargs)
               
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
            
    def save(self, *args, **kwargs):
        print "Model RawAuthor save called"
              
        super(RawAuthor, self).save(*args, **kwargs)