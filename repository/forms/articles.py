import os, sys, traceback
from django.forms import ModelForm

from repository.models import Poetry, Snippet

class PoetryForm(ModelForm): 
       
    class Meta:
        model = Poetry
        fields = '__all__'
        #fields = ['name', 'name_en', 'sobriquet', 'date_birth', 'date_death', 'image', 'summary', 'source_url']                          

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(PoetryForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj
    

class SnippetForm(ModelForm): 
       
    class Meta:
        model = Snippet
        fields = '__all__'
        #fields = ['name', 'name_en', 'sobriquet', 'date_birth', 'date_death', 'image', 'summary', 'source_url']                          

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(SnippetForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj    