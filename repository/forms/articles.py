import os, sys, traceback
from django.forms import ModelForm

from repository.models import Poetry, Snippet, Person

class PoetryForm(ModelForm): 
       
    class Meta:
        model = Poetry
        fields = ['name', 'description', 'same_as', # Thing
                  'creator', 'license', 'keywords', # CreativeWork
                  'language', 'body'                # Article
                  ]

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        ## Set the queryset as Empty Query Set. We will get the creator options later on using ajax request
        # NOTE: Comment following line, if you are not using ajax request to select creator
        if self.instance.id is None:
            self.fields['creator'].queryset = Person.objects.none()
        else:
            self.fields['creator'].queryset = Person.objects.filter(id__exact=self.instance.creator.id)
                
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
      