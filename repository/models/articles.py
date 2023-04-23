from django.db import models
from django.contrib import auth
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import default
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.utils import truncatelines

from .creative_works import Article

# Create your models here.


class Snippet(Article):
    '''
    @summary: An article, such as a news article or piece of investigative report.
    Newspapers and magazines have articles of many different types and this is intended to cover them all.
    @note: 
    
    '''
