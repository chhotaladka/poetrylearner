from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

# Create your models here.
       
        
class Reference(models.Model):
    '''
    Resource(s) used in the creation of a creative work. 
    A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.
    '''
    
    body = models.TextField(null=False,
                            help_text=_('List of references.')
                            )
    




class Tag(TagBase):
    # ... fields here

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    # ... methods (if any) here


class TaggedItem(GenericTaggedItemBase):
    # TaggedItem can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(Tag,
                            related_name="%(app_label)s_%(class)s_items")
    
    

def image_upload_path(instance, filename):
    """
    function for `upload_to` for ImageField
    file will be uploaded to `MEDIA_ROOT`/repository/images/%(class)_<first word of `name`>
    """

    file_type = filename.split('.')[-1]
    new_name = instance.name.split(' ')[0]
    new_name = new_name.lower() + '.' + file_type
    
    print( "saving item image " + filename + " as " + new_name)
    return 'repository/images/{c}_{name}'.format(c=type(instance).__name__.lower(), name=new_name)    