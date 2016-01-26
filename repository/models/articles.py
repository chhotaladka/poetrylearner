from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from django.template.defaultfilters import default
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from common.utils import truncatelines

from creative_works import Article

# Create your models here.

        
class Poetry(Article):
    '''
    @summary: A poetic article.
    @note: 
    
    '''
    class Meta:
        verbose_name = _("Poetry")
        verbose_name_plural = _("Poetries")  
        
    def summary(self):
        """
        Content to share on social media sites
        e.g. first stanza
        """
        return truncatelines(self.body, 4)          
    

class Snippet(Article):
    '''
    @summary: An article, such as a news article or piece of investigative report.
    Newspapers and magazines have articles of many different types and this is intended to cover them all.
    @note: 
    
    '''