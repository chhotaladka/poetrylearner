import os, sys, traceback
from django.forms import ModelForm
from django.forms.models import  ModelChoiceField
from django.core.exceptions import ValidationError

from repository.models import Snippet


class SnippetForm(ModelForm): 
       
    class Meta:
        model = Snippet
        fields = ['name', 'description', 'same_as', # Thing
                  'license', 'keywords', # CreativeWork
                  'body' # Article
                  ]

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj    
      