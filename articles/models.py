from django.db import models
from django.contrib import auth
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify

from projects.models import Author, Book


# Create your models here.


class ArticleMeta(models.Model):
    """
    Meta data for Article
    """    
    date_added = models.DateTimeField("first added on", auto_now_add=True)
    date_modified = models.DateTimeField("last modified on")
    date_published = models.DateTimeField("published on", null=True, blank=True)
    date_verified = models.DateTimeField("verified on", null=True, blank=True)
    
    is_published = models.BooleanField("published", default=False)
    is_verified = models.BooleanField("verified", default=False)
    proofread_level = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False);
    # True, if currently being held by a user for editing
       
    def __str__(self):          # on Python 3
        return str(self.id)
    
    def __unicode__(self):      # on Python 2
        return str(self.id)
    
           
    def save(self, *args, **kwargs):
        print "DEBUG: Model ArticleMeta save called"
        if self.is_published == True:
            self.date_published = timezone.now()
        
        if self.is_verified == True:
            self.date_verified = timezone.now()
              
        super(ArticleMeta, self).save(*args, **kwargs)
               
         

class Article(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=False)
    page_num = models.PositiveIntegerField("page number", default=0)
    
    book = models.ForeignKey(Book, related_name="articles", null=True, blank=True)
    author = models.ForeignKey(Author, related_name='articles')
    
    added_by = models.ForeignKey(auth.models.User, related_name="added_articles")
    modified_by = models.ForeignKey(auth.models.User, related_name="updated_articles")    
    meta = models.ForeignKey(ArticleMeta, related_name='article', null=True, blank=True)
    
    friendly_name = _("post")

    def __str__(self):          # on Python 3
        return self.title
    
    def __unicode__(self):      # on Python 2
        return self.title
  
    def get_title(self):
        return self.title
    
    def get_slug(self):
        """
        Returns the slugified title of the Article
        It can be used in the URL of Article related page
        """
        return str(slugify(self.title))

    def get_absolute_url(self):     
        kwargs = {'pk': str(self.id), 'slug': self.get_slug()}
        return reverse('articles:article-details', kwargs=kwargs)            

    def get_author(self):
        return self.author
    
    def get_book(self):
        return self.book
    
       
    def save(self, *args, **kwargs):
        print "DEBUG:: Model Article save called"
        
        # Save the Article
        super(Article, self).save()
                      
        create_meta = False
        
        if self.meta:
            print "DEBUG:: meta found"
            # Update ArticleMeta
            try:
                m = ArticleMeta.objects.get(pk=self.meta.id)
                print "DEBUG:: meta"
                m.is_verified = kwargs.get('is_verified', False)
                m.is_published = kwargs.get('is_published', False)
                
                ##
                # If proofreading has been finished by the user,
                # increase the proofread_level by ONE
                
                if kwargs.get('submit', False):
                    m.proofread_level = m.proofread_level + 1
                
                m.date_modified = timezone.now()
                
                m.save()
        
            except ArticleMeta.DoesNotExist:
                print "DEBUG:: meta not exist"
                create_meta = True
        else:
            create_meta = True
                
        if create_meta:
            print "DEBUG:: create meta"
            # Create a new ArticleMeta entry            
            m = ArticleMeta()
            m.date_modified = timezone.now()
            m.save()            
            self.meta = m      
        
        # Save the Article
        super(Article, self).save()