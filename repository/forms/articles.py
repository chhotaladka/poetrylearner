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
        obj = super(PoetryForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj
    

class SnippetForm(ModelForm): 
       
    class Meta:
        model = Snippet
        fields = ['name', 'description', 'same_as', # Thing
                  'media', 'creator', 'contributor', 'publisher', 'license', 'keywords', # CreativeWork
                  'language', 'body' # Article
                  ]

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(SnippetForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj    