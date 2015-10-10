from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
import os, sys, traceback
from django.conf import settings
from django.core import validators

from django_select2.fields import AutoModelSelect2MultipleField, AutoModelSelect2TagField
from django_select2.widgets import AutoHeavySelect2TagWidget
from django.core.exceptions import ObjectDoesNotExist
import json

from snippets.models import Snippet
from projects.models import Author


class SnippetForm(ModelForm): 
       
    class Meta:
        model = Snippet
        fields = ['title', 'body', 'language', 'author']                  
               
        
    def __init__(self, *args, **kwargs):
        super(SnippetForm, self).__init__(*args, **kwargs)
        
        # get the address to redirect, used by CANCEL button
        # Default is redirect to Home Page
        previous = "/"
        try:
            previous = kwargs.pop('previous')          
        except:
            pass
            
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Fieldset(
                'Add a snippet',
                Field('title', autocomplete='off', placeholder='Title', css_class='input-sm'),
                Field('body', css_class='input-sm'),
                Field('author', css_class='input-sm'),
                Field('language', css_class='input-sm'),
            ),
        
            FormActions(
                Submit('submit', 'Save changes'),
                Button('cancel', 'Cancel', onclick="location.href='{0}'".format(previous))
            ),
        
        )
                
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(SnippetForm, self).save(commit=False, *args, **kwargs)
        
        if obj.pk:          
            obj.updated_by = owner
        else:
            obj.added_by = owner
            obj.updated_by = owner
            
        if commit:
            obj.save()
        return obj