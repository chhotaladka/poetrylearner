from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
import os, sys, traceback
from django.conf import settings
from django.core import validators

from django.core.exceptions import ObjectDoesNotExist
import json

from snippets.models import Snippet
from projects.models import Author


class SnippetForm(ModelForm): 
       
    class Meta:
        model = Snippet
        fields = ['title', 'body', 'language', 'author', 'tags']
                
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(SnippetForm, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj