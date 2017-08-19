import os, sys, traceback
from repository.forms import BaseForm

from repository.models import Organization, Product, Person, Place, Event


class ProductForm(BaseForm):
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'same_as', # Thing
                  'manufacturer', 'image', 'is_related_to', 'is_similar_to'] # Product

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

        
class EventForm(BaseForm):
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'same_as', # Thing
                   'location', 'start_date', 'end_date', 'super_event', 'image'] # Event

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['super_event'].queryset = Event.objects.exclude(
            id__exact=self.instance.id)

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj        


class OrganizationForm(BaseForm):
    
    class Meta:
        model = Organization
        fields = ['name', 'description', 'same_as', # Thing
                  'address', 'parent', 'type']      # Organization

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['parent'].queryset = Organization.objects.exclude(
            id__exact=self.instance.id)
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj

class PlaceForm(BaseForm):
    
    class Meta:
        model = Place
        fields = ['name', 'description', 'same_as', # Thing
                  'address', 'has_map']             # Place

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj

class PersonForm(BaseForm):
    
    class Meta:
        model = Person
        fields = ['name', 'description', 'same_as', # Thing
                  'additional_name', 'affiliation', 'year_birth', 'year_death', 
                  'gender', 'image']                # Person

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(self.__class__, self).save(commit=False, *args, **kwargs)        
            
        if commit:
            obj.save()
        return obj
      
    