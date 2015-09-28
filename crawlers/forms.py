from django import forms
from django.forms import ModelForm
from crawlers.models import RawArticle

        
class RawArticleForm(ModelForm):
       
    class Meta:
        model = RawArticle
        fields = ['source_url', 'content']

        
