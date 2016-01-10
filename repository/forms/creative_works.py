import os, sys, traceback
from django.forms import ModelForm

from repository.models import Book

class BookForm(ModelForm): 
       
    class Meta:
        model = Book
        fields = '__all__'
        #fields = ['name', 'name_en', 'sobriquet', 'date_birth', 'date_death', 'image', 'summary', 'source_url']                          

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(BookForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj