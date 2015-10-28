from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.text import slugify
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from projects.helper.logs import print_log
from django.conf import settings
import os
import json
from urlparse import urlparse


# Create your models here.


def user_directory_path(instance, filename):
    """
    function for `upload_to` in `Author.image` ImageField
    file will be uploaded to `MEDIA_ROOT`/projects/author/<id>_<first word of `get_display_name`>
    """

    file_type = filename.split('.')[-1]
    new_name = instance.get_display_name().split(' ')[0]
    new_name = new_name.lower() + '.' + file_type
    
    print_log( "saving author.image " + filename + " as " + new_name)
    return 'projects/author/dp{id}_{name}'.format(id=instance.id, name=new_name)

class Author(models.Model):
    
    name = models.CharField(_('name'), max_length=200)
    name_en = models.CharField(_('name in English'), max_length=200, null=True, blank=True)
    sobriquet = models.CharField(_('also known as'), max_length=200, null=True, blank=True)
    date_birth = models.DateField(_('date of birth'), null=True, blank=True)
    date_death = models.DateField(_('date of death'), null=True, blank=True)
    image = models.ImageField(_('profile picture'), upload_to=user_directory_path, null=True, blank=True)
    summary = models.TextField(_('short introduction'), null=True, blank=True)
    source_url = models.URLField(_('Reference URL'), null=True, blank=True)
    
    date_modified = models.DateTimeField(_('last modified on'), auto_now=True)
    modified_by = models.ForeignKey(auth.models.User, null=True, blank=True, 
                                    related_name="updated_authors", verbose_name=_('last modified by'))


    def __str__(self):          # on Python 3
        return self.name
    
    def __unicode__(self):      # on Python 2
        return self.name
    
    def get_recent_books(self):
        """
        Get 5 recently added `Book`s of the `Author` in our records
        """        
        books = self.books.order_by('-date_modified')[:5]
        return books
    
    def get_name(self):
        return self.name

    def get_name_in_english(self):
        return self.name_en
        
    def get_sobriquet(self):
        return self.sobriquet
    
    def get_date_birth(self):
        return self.date_birth
    
    def get_date_death(self):
        return self.date_death
    
    def get_summary(self):
        return self.summary
    
    def get_source_url(self):
        return self.source_url
    
    def get_source_name(self):
        # Returns domain name from the `source_url` 
        return urlparse(self.source_url).netloc    
    
    def get_last_edit_time(self):
        return self.date_modified
    
    def get_last_edit_user(self):
        return self.modified_by
        
    def get_display_name(self):
        """
        Returns display name of Author
        """
        if self.sobriquet:
            return self.sobriquet         
        elif self.name_en:
            return self.name_en       
        else:
            return self.name
        
    def get_slug(self):
        """
        Returns the slugified display name of the Author
        It can be used in the URL of Author related page
        """
        if self.name_en:
            name = self.name_en
        elif self.sobriquet:
            name = self.sobriquet
        else:
            name = self.name
        
        return str(slugify(name))
        
    def get_absolute_url(self):     
        kwargs = {'pk': str(self.id), 'slug': self.get_slug()}
        return reverse('projects:author-details', kwargs=kwargs)
    
    def get_image_url(self):
        """
        Returns default Author image if `self.image` is None
        """
        if self.image:
            return '{0}{1}'.format(settings.MEDIA_URL, self.image)            
        else:
            default_img = 'img/author.jpg'
            return '{0}{1}'.format(settings.STATIC_URL, default_img)  
    
    def clean(self):
        print "DBG:: Model Auhtor clean called"
        # date_death must be greater than date_birth
        if self.date_death is not None and self.date_death is not None:
            if self.date_death < self.date_birth:
                raise ValidationError({
                    'date_death': "Foeticide is illegal. Death shouldn't happen before birth."
                })
    
    def save(self, *args, **kwargs):
        print "DBG:: Model Auhtor save called"
        self.name = self.name.title()
        
        if self.sobriquet:
            # This filed `sobriquet` is optional, so it needs to be checked whether it is passed or not
            # (In case you have called save without using any Form)
            self.sobriquet = self.sobriquet.title()
        if self.name_en:
            self.name_en = self.name_en.title()
        
        super(Author, self).save(*args, **kwargs)
      
        

class Book(models.Model):
    
    name = models.CharField(_('original title'), max_length=200)
    authors = models.ManyToManyField(Author, related_name='books', verbose_name=_('authors name'))
    pid = models.CharField(_('Published IDs'), max_length=255, null=True, blank=True)
    publisher = models.CharField(_('publisher'), max_length=200, null=True, blank=True)
    year_published = models.PositiveIntegerField(_('year of publication'), null=True, blank=True)
    language = models.CharField(_('language'), max_length=32, choices = LANGUAGES, default='hi')
    
    date_modified = models.DateTimeField(_('last modified on'), auto_now=True)
    modified_by = models.ForeignKey(auth.models.User, related_name="updated_books", verbose_name=_('last modified by'))
        
    def __str__(self):          # on Python 3
        return self.name
    
    def __unicode__(self):      # on Python 2
        return self.name
    
    def get_title(self):
        return self.name
    
    def get_id_name(self):
        p = json.loads(self.pid)
        return p['name']

    def get_id_value(self):
        p = json.loads(self.pid)
        return p['value']

    def get_language(self):
        tmp = dict(LANGUAGES)
        return tmp[self.language]
    
    def get_year(self):
        # Get year of publication
        return self.year_published
    
    def get_publisher(self):
        return self.publisher
    
    def get_last_edit_time(self):
        return self.date_modified
    
    def get_last_edit_user(self):
        return self.modified_by
            
    def get_slug(self):
        """
        Returns the slugified name of the `Book`
        It can be used in the URL of `Book` related page
        """
        name = self.name
        return str(slugify(name))
    
    def get_absolute_url(self):
        kwargs = {'pk': str(self.id),'slug': self.get_slug()}
        return reverse('projects:book-details', kwargs=kwargs)
    
    def save(self, *args, **kwargs):
        print "DBG:: Model Book save called"
        # Capitalize first alphabet of each word in `name` 
        self.name = self.name.title()
               
        super(Book, self).save(*args, **kwargs)
    
    
class Project(models.Model):
    """
    Project Model
    """
    # Available choices for source field
    SOURCES = (
        ('offline', 'Scanned by ourself'),
        ('online', 'Online digital library'),
    )
    
    # Project States
    PROJECT_STATES = (
        (1, 'Project Initiation'),
        (2, 'Adding Scanned Data'),
        (3, 'Adding OCR Data'),
        (4, 'In Proofreading Rounds'),
        (5, 'In Formatting Rounds'),
        (6, 'Project Published'),
    ) 

    book = models.ForeignKey(Book, related_name="project")
    source = models.CharField(max_length=32, choices = SOURCES, default='offline')
    source_url = models.URLField(max_length=1000, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pages = models.PositiveIntegerField(_('total pages'), default=0)
    scanned_pages = models.PositiveIntegerField(_('number of scanned pages'), default=0)
    contributors = models.ManyToManyField(auth.models.User, related_name='projects', blank=True)
    manager = models.ForeignKey(auth.models.User)
    
    date_modified = models.DateTimeField(_('last modified on'), auto_now=True)
  
    note = models.TextField(_('Leave a note'), null=True, blank=True)
    state = models.PositiveIntegerField(_('project state'), choices = PROJECT_STATES, default=1)
    
    def __str__(self):          # on Python 3
        return self.book.name
    
    def __unicode__(self):      # on Python 2
        return self.book.name
        
    def get_slug(self):
        """
        Returns the slugified name of the `Project`
        It can be used in the URL of `Project` related page
        """
        name = self.book.name
        return str(slugify(name))
    
    def get_absolute_url(self):
        kwargs = {'pk': str(self.id),'slug': self.get_slug()}
        return reverse('projects:project-details', kwargs=kwargs)
    
    def get_source_name(self):
        tmp = dict(self.SOURCES)
        return tmp[self.source]

    def get_state_name(self):    
        tmp = dict(self.PROJECT_STATES)
        return tmp[self.state]
    
    @classmethod
    def get_all_states(cls):
        """
        Returns all states
        """
        return cls.PROJECT_STATES 
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
    def get_pages_num(self):
        return self.pages
    
    def get_scanned_pages_num(self):
        return self.scanned_pages
    
    def get_note(self):
        return self.note
    
    def get_last_edit_time(self):
        return self.date_modified
    
    def get_last_edit_user(self):
        return self.manager    
    
    def get_pages(self):
        """
        Returns range of total number of pages in the Book
        """
        return range(1, self.pages+1)

    def get_scanned_pages(self):
        """
        Returns range of total number of scanned pages
        """
        return range(1, self.scanned_pages+1)
            
    def get_dir(self):
        """
        Get the project directory
        """
        return '{mediaroot}/projects/{id}_book'.format(mediaroot=settings.MEDIA_ROOT, id=self.id)
    
    def get_path_img_scanned(self):
        """
        Get the path of archive file of the raw scanned images
        __projectid_img_scanned.tar__
        """
        return '{base}/{id}_img_scanned.tar'.format(base=self.get_dir(), id=self.id)

    def get_path_img_jp2(self):
        """
        Get the path of archive file of the processed JPEG2000 images
        __projectid_img_jp2.tar__
        """
        return '{base}/{id}_img_jp2.tar'.format(base=self.get_dir(), id=self.id)

    def get_path_ocr(self):
        """
        Get the path of archive file of the OCR data XML format.
        __projectid_ocr.tar__
        """
        return '{base}/{id}_ocr.tar'.format(base=self.get_dir(), id=self.id)            

    def get_path_ebooks(self):
        """
        Get the path of archive file of the finished eBooks.
        __projectid_ebooks.tar__
        """
        return '{base}/{id}_ebooks.tar'.format(base=self.get_dir(), id=self.id) 
    
    def get_path_meta(self):
        """
        Get the path of JSON file containing bibliographic metadata about the book.
        __projectid_meta.json__
        """
        return '{base}/{id}_meta.json'.format(base=self.get_dir(), id=self.id) 
           
           
    def clean(self):
        # source_url is required if the source selected is 'online`
        if self.source == 'online' and len(self.source_url) == 0:
            raise ValidationError({
                'source_url': "This filed is required for the slected Source."
            })
                       
    def save(self, *args, **kwargs):
        print "DBG:: Model Project save called"              
        super(Project, self).save(*args, **kwargs)
        
        """
        Create the directory for Project
        """
        try:
            if not os.path.exists(self.get_dir()):
                os.makedirs(self.get_dir(), mode=0755)
        except OSError, err:
            print 'ERROR:: while creating project dir: %s' % (err)
        
        

class ImageSource(models.Model):
    """
    Image Source Model for scanned images
    """
    page_num = models.PositiveIntegerField(_('page number'), default=0)
    url = models.URLField(max_length=1000, null=True, blank=True)
    note = models.CharField(max_length=140, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='image_source')
    
    def save(self, *args, **kwargs):
        print "Model ImageSource save called"
          
        super(ImageSource, self).save(*args, **kwargs)
                   

                     
class Page(models.Model):
    """
    Pages of a Book
    """
    
    body = models.TextField(null=False)
    
    book = models.ForeignKey(Book, related_name="pages")
    page_num = models.PositiveIntegerField('page number', default=0)
    author = models.ForeignKey(Author, related_name='pages')
    
    added_by = models.ForeignKey(auth.models.User, related_name='added_pages')
    added_at = models.DateTimeField(auto_now_add=True)
    
    updated_by = models.ForeignKey(auth.models.User, related_name='updated_pages')
    updated_at = models.DateTimeField(auto_now=True)  

    proofread_level = models.PositiveIntegerField(default=0)
        
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=False); # True, if currently being held by a user for editing
    

    def __str__(self):          # on Python 3
        return self.page_num
    
    def __unicode__(self):      # on Python 2
        return self.page_num


    def get_author(self):
        return self.author
    
    def get_book(self):
        return self.book
    
    def get_absolute_url(self):     
        kwargs = {'page_num': str(self.page_num), 'pk': str(self.book.id)}
        return reverse('projects:book-page', kwargs=kwargs)  
       
    def save(self, *args, **kwargs):
        print "DEBUG:: Model Page save called"  
        super(Page, self).save()
        
        # If proof-reading has been finished by the user,
        # increase the proofread_level by ONE        
        if kwargs.get('submit', False):
            self.proofread_level = m.proofread_level + 1                      
        
        if self.verified == True:
            self.verified_at = timezone.now()
        
        # Save    
        super(Page, self).save()
