from django.shortcuts import render, get_object_or_404
from django.views.generic import *
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crawlers.models import RawArticle

# Create your views here.

"""
Details of the RawArticle
"""
def raw_article_details(request, pk):
    obj = get_object_or_404(RawArticle, pk=pk)
    
    data = json.loads(obj.content)
    # data contains ['index', 'title', 'author', 'poem', 'url']
        
    context = {'article': obj, 'data': data}
    template = "crawlers/article-details.html"

    return render(request, template, context)


def raw_article_list(request):
    """
    
    """    
    
    # Get the object list           
    obj_list = RawArticle.objects.all()
    
    ##
    # Check the parameters passed in the URL and process accordingly

    
    ##
    # Check for permissions and render the list of articles
    
    
    # Pagination
    paginator = Paginator(obj_list, 20) # Show 20 articles per page    
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
            
    context = {'articles': articles}
    template = 'crawlers/article-list.html'    

    return render(request, template, context)