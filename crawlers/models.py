from django.db import models
from datetime import datetime
from django.contrib import auth
from articles.models import Article

# Create your models here.

#
# Crawled articles from accros the web by web spiders (scrapy)
#
class RawArticle(models.Model):
            
    source_url = models.URLField(null=False, max_length=1000)
    content = models.TextField(null=False)
    date_added = models.DateTimeField("added on", auto_now_add=True)
    is_valid = models.BooleanField("valid", default=False)
    article = models.ForeignKey(Article, related_name='ref_crawled', null=True, blank=True, verbose_name="related entry in article table")
    

    def __str__(self):          # on Python 3
        return self.source_url
    
    def __unicode__(self):      # on Python 2
        return self.source_url
      
    def get_absolute_url(self):
        pass
    
    
    def save(self, *args, **kwargs):
        print "Model RawArticle save called"
              
        super(RawArticle, self).save(*args, **kwargs)
               
