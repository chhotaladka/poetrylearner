from django.shortcuts import render, get_object_or_404
from django.views.generic import *
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from crawlers.models import RawArticle, RawAuthor

# Create your views here.

def make_cond(name, value):
    """
    Convert normal name, value to json key:value pair
    """     
    cond = json.dumps({name:value})[1:-1] # remove '{' and '}'
    return ' ' + cond # avoid '\"'

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
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly
    view_type = request.GET.get('view', None)
    source = request.GET.get('source', None)
    title = request.GET.get('title', None)
    author = request.GET.get('author', None)
    filters = request.GET.get('filters', None)
    
    if filters:
        filters = filters.split(',')
        print filters
        # Supported filters are: valid, invalid, snippet, nosnippet
        if 'valid' in filters:
            q_objects &= Q(valid=True)
        elif 'invalid' in filters:
            q_objects &= Q(valid=False)
        if 'snippet' in filters:
            q_objects &= ~Q(snippet=None)
        elif 'nosnippet' in filters:
            q_objects &= Q(snippet=None)
    
    
    if source:
        # filter the source_url
        q_objects &= Q(source_url__icontains=source)
    
    if title:
        pass
    
    if author:
        pass
    
    # Get all articles           
    obj_list = RawArticle.objects.all().filter(q_objects)      
    
       
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


def raw_author_details(request, pk):
    obj = get_object_or_404(RawAuthor, pk=pk)
        
    context = {'author': obj}
    template = "crawlers/author-details.html"

    return render(request, template, context)


def raw_author_list(request):
    """
    List view
    """    
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    source = request.GET.get('source', None)
    name = request.GET.get('name', None)    
    filters = request.GET.get('filters', None)
    
    if filters:
        filters = filters.split(',')        
        # Supported filters are: valid or invalid, birth or nobirth, death or nodeath
        if 'valid' in filters:
            q_objects &= Q(valid=True)
        elif 'invalid' in filters:
            q_objects &= Q(valid=False)
        if 'birth' in filters:
            # get the authors whom birth info is known
            q_objects &= ~Q(birth=None)
        elif 'nobirth' in filters:
            # get the authors whom birth info is not known
            q_objects &= Q(birth=None)
        if 'death' in filters:
            # get the authors whom death info is known
            q_objects &= ~Q(death=None)
        elif 'nodeath' in filters:
            # get the authors whom death info is not known
            q_objects &= Q(death=None)            

    if source:        
        # filter with source_url
        q_objects &= Q(source_url__icontains=source)

    if name:        
        # get the authors with 'name'        
        q_objects &= Q(name__icontains=name)        
                
    # Get all authors           
    obj_list = RawAuthor.objects.all().filter(q_objects)
    
    ##
    # Check for permissions and render the list of authors
    
    
    # Pagination
    paginator = Paginator(obj_list, 20) # Show 20 authors per page    
    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authors = paginator.page(paginator.num_pages)
            
    context = {'authors': authors}
    template = 'crawlers/author-list.html'    

    return render(request, template, context)


def dashboard(request):
    author = {}
    article = {}
    
    author['total'] = RawAuthor.objects.all().count
    author['valid'] = RawAuthor.objects.valid().count
    author['nobirth'] = RawAuthor.objects.nobirth().count
    author['nodeath'] = RawAuthor.objects.nodeath().count
    author['nodate'] = RawAuthor.objects.nodate().count
    
    article['total'] = RawArticle.objects.all().count
    article['valid'] = RawArticle.objects.valid().count
    article['withsnippet'] = RawArticle.objects.withsnippet().count        
        
    context = {'author': author, 'article': article}
    template = "crawlers/dashboard.html"

    return render(request, template, context)