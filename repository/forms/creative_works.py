import os, sys, traceback
from django.forms.models import ModelChoiceField
from django.core.exceptions import ValidationError

from repository.forms import BaseForm
from repository.models import Poetry, Book, Person
from taggit.forms import TagField
from taggit.utils import split_strip


class Select2ChoiceField(ModelChoiceField):
    '''
    In case you are populating the fields using ajax request then 'to_python' must be 
    overridden, as default queryset is None and this function originally check if 
    returned value is in the queryset which in turns raise validation error "invalid_choice".
    '''
                
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            #MODIFIED HERE: check for value in all object instead of self.queryset
            value = self.queryset.model.objects.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
        return value


class BookForm(BaseForm): 
    
    creator = Select2ChoiceField(queryset=Person.objects.filter())
    
    class Meta:
        model = Book
        fields = ['name', 'description', 'same_as', # Thing
                  'creator', 'contributors', 'publisher', 'license', 'keywords', # CreativeWork
                  'language', 'isbn'] # Book

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        ## Set the queryset for `creator` field.
        # We will get the creator options later on using ajax request
        person_queryset = Person.objects.none()
        if self.instance.id:
            person_queryset = Person.objects.filter(id__exact=self.instance.creator.id)
        else:
            if kwargs.get('initial', None):
                if 'creator' in kwargs.get('initial'):
                    person_queryset = Person.objects.filter(id__exact=kwargs.get('initial')['creator'])
        self.fields['creator'].queryset = person_queryset
    
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(BookForm, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj


class TaggitTagField(TagField):
    '''
    Added has_changed method in TagField
    '''
    def has_changed(self, initial, data):
        initial_list = [i.tag.name for i in initial]
        data_list = split_strip(data, ',')
        
        if len(initial_list) != len(data_list):
            return True
        initial_set = set(value for value in initial_list)
        data_set = set(value for value in data_list)
        return data_set != initial_set


class PoetryForm(BaseForm):
    
    creator = Select2ChoiceField(queryset=Person.objects.filter())
    keywords = TaggitTagField(required=False)

    class Meta:
        model = Poetry
        fields = ['name', 'description', 'same_as', # Thing
                  'creator', 'license', 'keywords', # CreativeWork
                  'language', 'body'                # Article
                  ]

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        ## Set the queryset for `creator` field.
        # We will get the creator options later on using ajax request
        person_queryset = Person.objects.none()
        if self.instance.id:
            person_queryset = Person.objects.filter(id__exact=self.instance.creator.id)
        else:
            if kwargs.get('initial', None):
                if 'creator' in kwargs.get('initial'):
                    person_queryset = Person.objects.filter(id__exact=kwargs.get('initial')['creator'])
        self.fields['creator'].queryset = person_queryset
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)

        if commit:
            obj.save()
        return obj
    