from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class BookmarkManager(models.Manager):
    '''
    Manager for `Bookmark` model
    '''
    def get_for_user(self, obj, user):
        """
        Get the Bookmark made on the given object by the given user, or
        ``None`` if no matching bookmark exists.
        """
        if not user.is_authenticated:
            return None
        content_object = ContentType.objects.get_for_model(obj)
        try:
            obj = self.get(user=user, content_type=content_object, object_id=obj._get_pk_val())
      
        except ObjectDoesNotExist:
            #print 'No bookmark by {user} on {object}'.format(user=user, object=obj.id)
            return None
            
        return obj
    
    def get_all_for_user(self, user):
        '''
        Get all bookmarks by the ``user``
        '''
        bookmarks = self.filter(user=user)
        return bookmarks     
    
    def add_bookmark(self, obj, user):
        '''
        Create a user's bookmark on a given object. Only allows a given user
        to bookmark if it does not exist.                
        '''
        content_type = ContentType.objects.get_for_model(obj)
        # First, try to fetch the instance of this row from DB
        # If that does not exist, then it is the first time we're creating it
        # If it does, then just update the previous one
        try:
            bookmark_obj = self.get(user=user, content_type=content_type, object_id=obj._get_pk_val())
            print("WARNING:: bookmark already exist.")
                
        except ObjectDoesNotExist:
            #This is the first time we're creating it
            try:
                bookmark_obj = self.create(user=user, content_type=content_type, object_id=obj._get_pk_val())                        
            except:
                print('ERR:: something went wrong in creating a bookmark object. {file}:{line}'.format(file=str('__FILE__'), line=str('__LINE__')))
                bookmark_obj = None
        
        return bookmark_obj
    
    def remove_bookmark(self, obj, user):
        '''
        Remove a user's bookmark on a given object, if it exist.
        '''
        content_type = ContentType.objects.get_for_model(obj)
        try:
            bookmark_obj = self.get(user=user, content_type=content_type, object_id=obj._get_pk_val())
            bookmark_id = bookmark_obj.id
            bookmark_obj.delete()
                
        except ObjectDoesNotExist:
            print('WARNING:: Bookmark does not exist.')
            raise ObjectDoesNotExist  
        
        return bookmark_id 
    
    def get_bookmarks_count(self, obj):
        '''
        Get total number of current bookmarks by different users on a given object.
        '''
        if not obj:
            # Deleted object
            return 0

        content_type = ContentType.objects.get_for_model(obj)
        count = self.filter(content_type=content_type, object_id=obj._get_pk_val()).count()
        return count
    
    
class Bookmark(models.Model):
    '''
    @summary: Model for Bookmarks by user
    '''
    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="saved_bookmarks",
                             verbose_name=_("user")
                            )
    
    date_added = models.DateTimeField(auto_now_add=True,
                                      help_text=_("The date time on which the item was created or the item was added to a DataFeed.")
                                      )
    
    # Generic Foreign Key to the object this bookmark is about
    content_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    related_name="bookmark_content_objects",
                                    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    objects = BookmarkManager()
    
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):          # on Python 3
        return "{}'s bookmark".format(self.user.username)
    
    def __unicode__(self):      # on Python 2
        return "{}'s bookmark".format(self.user.username)
    
    def get_content_url(self):
        if self.content_object:
            return self.content_object.get_absolute_url()
        else:
            return ''
    
    def get_absolute_url(self):
        return self.get_content_url()  

    def title(self):
        return self.content_object.title() #TODO: do it without using content_object's title function    

    def save(self, *args, **kwargs):
        super(Bookmark, self).save(*args, **kwargs)
        
    def delete(self):
        super(Bookmark, self).delete()
