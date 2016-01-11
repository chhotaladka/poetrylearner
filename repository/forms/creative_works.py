import os, sys, traceback
from django.forms import ModelForm

from repository.models import Book

class BookForm(ModelForm): 
       
    class Meta:
        model = Book
        fields = ['name', 'description', 'same_as', # Thing
                  'creator', 'contributor', 'publisher', 'license', 'keywords', # CreativeWork
                  'language', 'isbn'] # Book

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(BookForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj