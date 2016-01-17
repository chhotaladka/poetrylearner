import os, sys, traceback
from django.forms import ModelForm

from repository.models import Poetry, Snippet

class PoetryForm(ModelForm): 
       
    class Meta:
        model = Poetry
        fields = ['name', 'description', 'same_as', # Thing
                  'creator', 'license', 'keywords', # CreativeWork
                  'language', 'body'                # Article
                  ]
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj
    

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
      