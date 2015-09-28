from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from crawlers.models import RawArticle

# Create your views here.

"""
Details of the RawArticle
"""
def RawArticleDetails(request, pk):
    a = get_object_or_404(RawArticle, pk=pk)
        
    context = {'article': a}
    template = "crawlers/article-details.html"

    return render(request, template, context)