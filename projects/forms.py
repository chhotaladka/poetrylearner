from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
import os, sys, traceback
from django.conf import settings
from projects.models import Project, Author, Book
from django.core import validators
from django_select2.fields import AutoModelSelect2MultipleField, AutoModelSelect2TagField
from django_select2.widgets import AutoHeavySelect2TagWidget
from django.core.exceptions import ObjectDoesNotExist
import json


PID_NAMES = (
        ('isbn-10', 'ISBN-10'),
        ('isbn-13', 'ISBN-13'),
    )

class AuthorForm(ModelForm): 
       
    class Meta:
        model = Author
        fields = ['name', 'name_en', 'sobriquet', 'date_birth', 'date_death', 'image', 'summary', 'source_url']                  
        
        help_texts = {            
            'name': 'Full name',
            'sobriquet': 'Penname or Nickname',
            'name_en': 'Name in English would help to optimize the search.',
            'date_birth': 'yyyy-mm-dd',
            'date_death': 'yyyy-mm-dd',
            'source_url': 'e.g. https://en.wikipedia.org/wiki/Kahlil_Gibran',
        }

    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(AuthorForm, self).save(commit=False, *args, **kwargs)
        obj.modified_by = owner
        if commit:
            obj.save()
        return obj
    

class CustomAutoHeavySelect2TagWidget(AutoHeavySelect2TagWidget):
    """
    The main reason behind adding this heavy things is, we don't want to use space 
    as tokenSeparator. 
    Apart from this, we can also manipulate inbuilt defaults of the widget.
    """

    def init_options(self):
        super(CustomAutoHeavySelect2TagWidget, self).init_options()
        self.options["tokenSeparators"] = [",",]
        
                
class AuthorChoices(AutoModelSelect2TagField):
    """
    The first instance of a class (sub-class) is used to serve all 
    incoming json query requests for that type (class).
    http://django-select2.readthedocs.org/en/latest/ref_fields.html?highlight=automodelselect2tagfield#django_select2.fields.AutoModelSelect2MultipleField
    """
    
    queryset = Author.objects.all()
    search_fields = ['name_en__icontains', 'name__icontains', 'sobriquet__icontains']
    max_results = 6
    
    def get_model_field_values(self, value):
        print "DBG:: get_model_field_values: ", value
        # NOTE: Make sure that `Author.modified_by` and other important fields are being updated
        # in the View.save() itself.
        return {'name': value}
    
    def extra_data_from_instance(self, obj):
        """
        Sub-classes should override this to generate extra data for values. These are passed to
        JavaScript and can be used for custom rendering.

        :param obj: The model object.
        :type obj: :py:class:`django.model.Model`

        :return: The extra data dictionary.
        :rtype: :py:obj:`dict`
        """
        try:
            print "DBG:: extra_data_from_instance"
            books = obj.books.all()[0:5]
            print books
            value = 'Known for ' + ', '.join([book.name for book in books])
            print "value: ", value
            
            extra_data = {}
            extra_data['books'] = value
            return extra_data
        except:
            print "ERRRRRRRR"
            pass
        
        return {}
    
            
class BookForm(ModelForm):
    """
    Part-I of the Project creation is adding the book information
    """
    
    authors = AuthorChoices(
                widget=CustomAutoHeavySelect2TagWidget(
                    select2_options={
                        'width': '-moz-available',
                        'placeholder': 'Search and select authors',
                        'allowClear': True,
                    }
                ),
            )
    
    pid_name = forms.ChoiceField(choices=PID_NAMES, required=False);
    pid_value = forms.CharField(max_length=64, required=False);  
        
    class Meta:
        model = Book
        fields = ['name', 'language', 'publisher', 'year_published']         
                       
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        
        #
        # Set initial for fields `pid_name` and `pid_value`
        if self.instance.id:
            try:
                pid = json.loads(self.instance.pid)
                self.fields['pid_name'].initial = pid['name']
                self.fields['pid_value'].initial = pid['value']
            except:
                print "ERROR:: No JSON object could be decoded"
                pass
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
            
            HTML("{{ wizard.management_form }}"),
            
            Fieldset(
                'Add book details',
                Field('name', autocomplete='off', css_class='input-sm'),
                Field('language', css_class='input-sm'),
                Field('authors', css_class='input-sm'),                
                Field('publisher', autocomplete='off', css_class='input-sm'),
                Field('year_published', autocomplete='off', css_class='input-sm'),
                Field('pid_name', css_class='input-sm'),
                Field('pid_value', autocomplete='off', css_class='input-sm'),
                
            ),
            
            FormActions(
                
                HTML("""
                    <input type="submit" name="submit" value="submit" class='btn btn-primary button col-lg-offset-2'/>            
                    {% if wizard.steps.prev %}
                        <button name="wizard_goto_step" type="submit" value="{{ wizard.steps.prev }}" class='btn btn-primary button'>previous step</button>
                    {% endif %}
                    
                """),
                Button('cancel', 'Cancel', onclick="location.href='{0}'".format(previous)),
            ),
        
        )
          
    def clean(self):
        """
        Check for the duplicate entry.
        If `name` matches, and at least one of its `authors` are same,
        then raise `ValidationError`
        """
        super(BookForm, self).clean()
        
        print "DBG:: BookForm checking duplicate"
        # validate, only if, at least `name' and 'authors` fields have been submitted in the form
        if self.cleaned_data.get('name', None) and self.cleaned_data.get('authors', None):
            try:            
                books = Book.objects.all().filter(name=self.cleaned_data['name']).exclude(id=self.instance.id)
                # The above .exclude(id=self.instance.id) part will work in case of update of existing Book

                if books:
                    for book in books:
                        authors = book.authors.all()
                        for a in self.cleaned_data['authors']:
                            if a in authors:                       
                                raise forms.ValidationError("Book already exists.")
                                   
            except ObjectDoesNotExist:
                print ("DBG:: Unexpected error:", sys.exc_info()[0])
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print ("DBG:: Error in %s on line %d" % (fname, lineno))
                pass
        
        #always return the cleaned data
        return self.cleaned_data
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(BookForm, self).save(commit=False, *args, **kwargs)
        print "DBG:: BookForm save"
        obj.modified_by = owner
        if commit:
            #
            # Make json data for pid field 
            if self.cleaned_data['pid_value']:
                pid = {}
                pid['name'] = self.cleaned_data['pid_name']
                pid['value'] = self.cleaned_data['pid_value']
                obj.pid = json.dumps(pid)                                
            
            obj.save()
            
            for author in self.cleaned_data['authors']:
                print "DBG:: Adding author ", author
                obj.authors.add(author)
            obj.save()
        return obj            

           
class ProjectForm(ModelForm):
    """
    Part-II of the Project creation
    """
    
    class Meta:
        model = Project
        fields = ['source', 'source_url', 'pages', 'note']
        
        help_texts = {
            'source': 'Source of the book.',
            'source_url': 'Web address of the book source.',
            'pages': 'Total number of pages in the book.',
        }

    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
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
                                    
            HTML("{{ wizard.management_form }}"),
                                                
            Fieldset(
                'A little more...',
                Field('source', css_class='input-sm'),
                Field('source_url', autocomplete='off', css_class='input-sm'),
                Field('pages', css_class='input-sm'),
                Field('note', css_class='input-sm'),
            ),
        
            FormActions(
                
                HTML("""
                    <input type="submit" name="submit" value="submit" class='btn btn-primary button col-lg-offset-2'/> 
                    {% if wizard.steps.prev %}
                        <button name="wizard_goto_step" type="submit" value="{{ wizard.steps.prev }}" class='btn btn-primary button'>previous step</button>
                    {% endif %}
                   
                """),
                Button('cancel', 'Cancel', onclick="location.href='{0}'".format(previous)),
            ),
        
        )
                
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(ProjectForm, self).save(commit=False, *args, **kwargs)
        
        # If fisrt time save i.e. project created
        manager = getattr(obj, 'manager', None)
        if manager is None:
            obj.manager = owner
            
        print "DBG:: ProjectForm save: book = ", obj.book
        
        if commit:
            obj.save()
        return obj
    

class UploadScannedImageForm(forms.Form):
    """
    For scanned images uploaded manually without using scrapy crawler
    """
    image = forms.ImageField()
    