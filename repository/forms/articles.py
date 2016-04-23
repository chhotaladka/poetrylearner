import os, sys, traceback
from django.forms import ModelForm
from django.forms.models import  ModelChoiceField
from django.core.exceptions import ValidationError

from repository.models import Poetry, Snippet, Person

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


class PoetryForm(ModelForm): 
    
    creator = Select2ChoiceField(queryset=Person.objects.filter())

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
      