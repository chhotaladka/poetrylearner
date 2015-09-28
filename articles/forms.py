from django import forms
from django.forms import ModelForm
from articles.models import Article
from projects.models import Author, Book
from django_select2.widgets import Select2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, HTML
from crispy_forms.bootstrap import FormActions

from django_select2.fields import AutoModelSelect2MultipleField, AutoModelSelect2TagField
from django_select2.widgets import AutoHeavySelect2TagWidget

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
    search_fields = ['name__icontains', 'sobriquet__icontains']
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
    

"""
help_texts for article's fields,
that can be accessed from multiple forms of `Article`     
"""
HTEXT_ARTICLE_NAME = 'Title of the article. Leave empty if unknown.'
HTEXT_ARTICLE_CONTENT = 'Content of the article.'
HTEXT_ARTICLE_PAGE= 'Page number of the book in which the article is published.'
               
class ArticleForm(ModelForm):

    author = AuthorChoices(
                widget=CustomAutoHeavySelect2TagWidget(
                    select2_options={
                        'width': '-moz-available',
                        'placeholder': 'Search and select the author',
                        'allowClear': True,                 
                    }
                ),
            )
           
    class Meta:
        model = Article
        fields = ['title', 'content', 'page_num', 'book', 'author']
        
#         widgets = {
#             'book': Select2Widget,
#             'auuthor': Select2Widget,
#         }
        
        labels = {
            'page_num': 'Page number',
        }
        help_texts = {
            'title': HTEXT_ARTICLE_NAME,
            'content': HTEXT_ARTICLE_CONTENT,
            'page_num': HTEXT_ARTICLE_PAGE,
        }

    
    def __init__(self, *args, **kwargs):       
        super(ArticleForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
                        
            Fieldset(
                'Add an article',
                Field('title', css_class='input-sm'),
                Field('content', css_class='input-sm'),
                Field('page_num', css_class='input-sm'),
                Field('book', css_class='input-sm'),
                Field('author', css_class='input-sm'),
            ),
        
            FormActions(
                Submit('submit', 'submit', css_class='button col-lg-offset-2'),
            ),
        
        )
        
    def save(self, owner, commit=True, *args, **kwargs):
        obj = super(ArticleForm, self).save(commit=False)
        
        obj.added_by = owner
        obj.modified_by = owner
        
        if commit:
            obj.save()
        return obj
    
        
class UpdateArticleForm(forms.Form):
     
    title = forms.CharField(max_length=200, required=False,
                            help_text=HTEXT_ARTICLE_NAME)
    content = forms.CharField(widget=forms.Textarea(),
                              help_text=HTEXT_ARTICLE_CONTENT)
    page_num = forms.IntegerField(label="Page number", min_value=0,
                                  help_text=HTEXT_ARTICLE_PAGE)
     
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
#     author = AuthorChoices(
#             widget=CustomAutoHeavySelect2TagWidget(
#                 select2_options={
#                     'width': '-moz-available',
#                     'placeholder': 'Search and select the author',
#                     'allowClear': True,
#                 }
#             ),
#         )
     
    is_published = forms.BooleanField(label="published",required=False)
    is_verified = forms.BooleanField(label="verified",required=False)

    
    def __init__(self, *args, **kwargs):       
        super(UpdateArticleForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Fieldset(
                'Add an article',
                Field('title', css_class='input-sm'),
                Field('content', css_class='input-sm'),
                Field('page_num', css_class='input-sm'),
                Field('book', css_class='input-sm'),
                Field('author', css_class='input-sm'),
                Field('is_published', css_class='input-sm'),
                Field('is_verified', css_class='input-sm'),
            ),
        
            FormActions(
                Submit('submit', 'submit', css_class='button white col-lg-offset-2'),
            ),
        
        )
        
    def save(self, owner, pk, commit=True, *args, **kwargs):
         
        obj = Article.objects.get(pk=pk)
        obj.title = self.cleaned_data['title']
        obj.content = self.cleaned_data['content']
        obj.page_num = self.cleaned_data['page_num']
        obj.book = self.cleaned_data['book']
        obj.author = self.cleaned_data['author']
        obj.modified_by = owner
         
        p = self.cleaned_data['is_published']
        v = self.cleaned_data['is_verified']
         
        if commit:
            obj.save(is_published=p, is_verified=v)
 
        return obj
        
                