from django.db import models
from django.contrib import auth
from django.conf.global_settings import LANGUAGES
from django.utils import timezone
from django.template.defaultfilters import default
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from projects.models import Author, Page
from tag import Tag

# Create your models here.


class Snippet(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=False)
    language = models.CharField(max_length=32, choices=LANGUAGES, default='hi')
    
    author = models.ForeignKey(Author, related_name='snippets')
    page = models.ForeignKey(Page, null=True, blank=True, related_name='snippets')
    
    added_by = models.ForeignKey(auth.models.User, related_name='added_snippets')
    added_at = models.DateTimeField(auto_now_add=True)
    
    updated_by = models.ForeignKey(auth.models.User, related_name='updated_snippets')
    updated_at = models.DateTimeField(auto_now=True)
    
    #tags = models.ManyToManyField('Tag', related_name='%(class)ss')
    
    published = models.BooleanField(default=False)

    class Meta:
        app_label = 'snippets'
        
    
    def __str__(self):          # on Python 3
        return self.title
    
    def __unicode__(self):      # on Python 2
        return self.title
  
    def get_title(self):
        return self.title
    
    def get_language(self):
        tmp = dict(LANGUAGES)
        return tmp[self.language]

    def get_slug(self):
        """
        TODO
        Returns the slugified title of the Snippet
        """
        return str(slugify(self.title))

    def get_absolute_url(self):     
        kwargs = {'pk': str(self.id), 'slug': self.get_slug()}
        return reverse('snippets:view', kwargs=kwargs)    

    def get_description(self):
        """
        Content to share on social media sites
        """
        #TODO return first stanza
        return self.body
    
#     def get_dirty_fields(self):
#         return [f.name for f in self._meta.fields if self._original_state[f.attname] != self.__dict__[f.attname]]
#     
#     def _list_changes_in_tags(self):
#         dirty = self.get_dirty_fields()
# 
#         if not 'tagnames' in dirty:
#             return None
#         else:
#             if self._original_state['tagnames']:
#                 old_tags = set(self._original_state['tagnames'].split())
#             else:
#                 old_tags = set()
#             new_tags = set(self.tagnames.split())
# 
#             return dict(
#                     current=list(new_tags),
#                     added=list(new_tags - old_tags),
#                     removed=list(old_tags - new_tags)
#                     )
#             
#             
#     def _process_changes_in_tags(self):
#         tag_changes = self._list_changes_in_tags()
# 
#         if tag_changes is not None:
#             for name in tag_changes['added']:
#                 try:
#                     tag = Tag.objects.get(name=name)
#                 except Tag.DoesNotExist:
#                     tag = Tag.objects.create(name=name, created_by=self.updated_by)
# 
#                 if not self.nis.deleted:
#                     tag.add_to_usage_count(1)
#                     tag.save()
# 
#             if not self.nis.deleted:
#                 for name in tag_changes['removed']:
#                     try:
#                         tag = Tag.objects.get(name=name)
#                         tag.add_to_usage_count(-1)
#                         tag.save()
#                     except:
#                         pass
# 
#             return True
# 
#         return False  
    
#     def save(self, *args, **kwargs):
#       
#         tags_changed = self._process_changes_in_tags()
#         
#         super(Snippet, self).save(*args, **kwargs)
#         if tags_changed:
#             if self.tagnames.strip():
#                 self.tags = list(Tag.objects.filter(name__in=self.tagname_list()))
#             else:
#                 self.tags = []              
        