import os, sys, traceback
from django.forms import ModelForm

from repository.models import Organization, Product, Person, Place, Event


class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ['added_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['is_related_to'].queryset = Product.objects.exclude(
            id__exact=self.instance.id)
        self.fields['is_similar_to'].queryset = Product.objects.exclude(
            id__exact=self.instance.id)

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj        

        
class EventForm(ModelForm):
    
    class Meta:
        model = Event
        exclude = ['added_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['super_event'].queryset = Event.objects.exclude(
            id__exact=self.instance.id)

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj        


class OrganizationForm(ModelForm):
    
    class Meta:
        model = Organization
        exclude = ['added_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['parent'].queryset = Organization.objects.exclude(
            id__exact=self.instance.id)
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj

class PlaceForm(ModelForm):
    
    class Meta:
        model = Place
        exclude = ['added_by', 'modified_by']

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj
                
class PersonForm(ModelForm):
    
    class Meta:
        model = Person
        exclude = ['affiliation', 'added_by', 'modified_by']

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj
      
    