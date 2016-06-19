from django.shortcuts import render, get_object_or_404
import os, sys, traceback
from django.views.generic import *
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from crawlers.models import RawArticle, RawAuthor
from django.utils.http import urlencode
from django.http import JsonResponse
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from common.utils import html_to_plain_text
from common.decorators import group_required

from repository.models import Poetry, Person 

# Create your views here.


"""
Details of the RawArticle
"""
@group_required('administrator')
def raw_article_details(request, pk):
    obj = get_object_or_404(RawArticle, pk=pk)    
        
    context = {'article': obj}
    template = "crawlers/article-details.html"

    return render(request, template, context)

@group_required('administrator')
def raw_article_list(request):
    """
    
    """    
    q_objects = Q()
    result_title = 'Articles'
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    # Query tab
    q_tab = request.GET.get('tab', None)
    # source url    
    source = request.GET.get('source', None)
    # author name
    author = request.GET.get('author', None)
    # search string
    q = request.GET.get('q', None)    

    # Process get queries
    if q_tab == 'all':
        q_objects = q_objects
    elif q_tab == 'valid':
        q_objects &= Q(valid=True)
    elif q_tab == 'invalid':
        q_objects &= Q(valid=False)            
    
    if source:
        source = source.strip()
        # filter the source_url
        q_objects &= Q(source_url__icontains=source)
        result_title = result_title + ', ' + source

    if author:
        author = author.strip()
        # filter the source_url
        q_objects &= Q(author__icontains=author)
        result_title = result_title + ', ' + author
    
    if q:
        q = q.strip()
        # TODO make it more perfect 
        q_objects &= Q(source_url__icontains=q) | Q(author__icontains=q) | Q(title__icontains=q) | Q(content__icontains=q)
        result_title = result_title + ', ' + q      
        
    # Get all articles              
    obj_list = RawArticle.objects.all().filter(q_objects)        
       
    # Create tab list and populate
    query_tabs = []    
    
    tab = {
           'name': 'all',
           'help_text': 'Recent items',
           'url': request.path + '?tab=all' + '&q=' + (q if q else '') + '&author=' + (author if author else ''),
           'css': 'is-active' if q_tab == 'all' or q_tab is None else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'valid',
           'help_text': 'Itmes which have been added to repository',
           'url': request.path + '?tab=valid' + '&q=' + (q if q else '') + '&author=' + (author if author else ''),
           'css': 'is-active' if q_tab == 'valid' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'invalid',
           'help_text': 'Itmes which have not added to repository',
           'url': request.path + '?tab=invalid' + '&q=' + (q if q else '') + '&author=' + (author if author else ''),
           'css': 'is-active' if q_tab == 'invalid' else '',
        }
    query_tabs.append(tab)
    
    
    # Pagination
    paginator = Paginator(obj_list, 40) # Show 40 articles per page    
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
            
    context = {'articles': articles,
               'query_tabs': query_tabs,
               'result_title': result_title}
    template = 'crawlers/article-list.html'    

    return render(request, template, context)


@group_required('administrator')
def raw_author_details(request, pk):
    obj = get_object_or_404(RawAuthor, pk=pk)
    # Number of articles by this author in the RawArticle
    articles = {}
    articles['total'] = RawArticle.objects.all().filter(author__icontains=obj.name).count()
    articles['new'] = RawArticle.objects.all().filter(author__icontains=obj.name).filter(valid=False).count()
    
    if request.is_ajax():
        # To set the validity
        valid = request.GET.get('valid', None)
        if valid is not None:
            obj.valid = bool(valid)
            obj.save()
            res = {}
            res['result'] = 'success'
            res['data'] = str(valid)             
            return JsonResponse(res)
        else:
            res = {}
            res['result'] = 'failure'                    
            return JsonResponse(res)
         
    context = {'author': obj, 'articles': articles}
    template = "crawlers/author-details.html"

    return render(request, template, context)


@group_required('administrator')
def article_to_poetry(request):
    '''
    Create poetries in Repository from given RawArticles
    '''
    ##
    # Check the parameters passed in the URL and process accordingly
    creator_id = request.GET.get('creator', None)
    article_ids = request.GET.get('articles', None)
            
    # Only AJAX POST request is allowed  
    if request.is_ajax() and request.method == "POST":    
        if creator_id is None or article_ids is None:
            # Return failure
            print "Error: article_to_poetry: No parameter(s) passed."                
            res = {}
            res['result'] = 'failure'
            res['count'] = 0                    
            return JsonResponse(res)
        
        article_ids = [x.strip() for x in article_ids.split(',')]
        # remove comma from the 
        if not article_ids[-1]:
            article_ids = article_ids[:-1]            
        creator_id = creator_id.strip()               
        print "article_to_poetry: creator=", creator_id, "articles=", article_ids            
        
        count = 0
        
        try:                                
            # Get the `Person` object having id=`creator_id`
            # Return failure if not found
            person = Person.objects.get(pk=creator_id)
            
            if person:            
                # Add all 'articles' to Poetry with 'person' as 'creator' field
                print "article_to_poetry: found ", person.name, " in person@repository"
                        
                for article_id in article_ids:
                    article = RawArticle.objects.get(pk=article_id)
                    
                    if article:
                        # Create a new poetry              
                        poetry = Poetry()
                        
                        poetry.name = article.title
                        poetry.language = article.language
                        poetry.body = html_to_plain_text(article.content)
                        poetry.creator = person
                        poetry.same_as = article.source_url
                        poetry.added_by = request.user
                        poetry.modified_by = request.user
                        poetry.save()
                        print "article_to_poetry: RawArticle ", article_id, "-> Poetry ", poetry.id
                        
                        # Make the raw_article valid
                        article.valid = True
                        article.save()
                        count += 1
                    
                # Return success with number of poetry made
                print "article_to_poetry: Total", count                        
                res = {}
                res['result'] = 'success'
                res['count'] = count  
                return JsonResponse(res)
    
            else:
                # Return failure, means You have to add the entry of Person first
                print "No such creator/person found in person@repository"
                
                res = {}
                res['result'] = 'failure'
                res['count'] = 0                    
                return JsonResponse(res)
            
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            res = {}
            res['result'] = 'error'
            res['count'] = 0                    
            return JsonResponse(res)           
            
    return HttpResponseForbidden()

@group_required('administrator')
def raw_author_list(request):
    """
    List view
    """    
    q_objects = Q()
    result_title = 'Authors'
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    # Query tab
    q_tab = request.GET.get('tab', None)
    # source url
    source = request.GET.get('source', None)
    # search string
    q = request.GET.get('q', None)

    # Process get queries
    if q_tab == 'all':
        q_objects = q_objects
    elif q_tab == 'valid':
        q_objects &= Q(valid=True)
    elif q_tab == 'invalid':
        q_objects &= Q(valid=False)
    elif q_tab == 'birth':
        # get the authors whom birth info is known
        q_objects &= ~Q(birth=None)
        q_objects &= ~Q(birth=u'')
    elif q_tab == 'death':
        # get the authors whom death info is known
        q_objects &= ~Q(death=None)
        q_objects &= ~Q(death=u'')          

    if source:
        source = source.strip()  
        # filter with source_url
        q_objects &= Q(source_url__icontains=source)
        result_title = result_title + ', ' + source
        
    if q:
        q = q.strip()      
        # get the authors with 'name'        
        q_objects &= Q(name__icontains=q) | Q(source_url__icontains=q)      
        result_title = result_title + ', ' + q
                
    # Get all authors           
    obj_list = RawAuthor.objects.all().filter(q_objects)        
    
    # Create tab list and populate
    query_tabs = []    
    tab = {
           'name': 'all',
           'help_text': 'Recent items',
           'url': request.path + '?tab=all' + '&q=' + (q if q else ''),
           'css': 'is-active' if q_tab == 'all' or q_tab is None else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'valid',
           'help_text': 'Itmes which have been added to repository',
           'url': request.path + '?tab=valid' + '&q=' + (q if q else ''),
           'css': 'is-active' if q_tab == 'valid' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'invalid',
           'help_text': 'Itmes which have not added to repository',
           'url': request.path + '?tab=invalid' + '&q=' + (q if q else ''),
           'css': 'is-active' if q_tab == 'invalid' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'birth known',
           'help_text': 'Birth date info available',
           'url': request.path + '?tab=birth' + '&q=' + (q if q else ''),
           'css': 'is-active' if q_tab == 'birth' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'death known',
           'help_text': 'Death date info available',
           'url': request.path + '?tab=death' + '&q=' + (q if q else ''),
           'css': 'is-active' if q_tab == 'death' else '',
        }
    query_tabs.append(tab)        
    
    
    # Pagination
    paginator = Paginator(obj_list, 40) # Show 40 authors per page    
    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authors = paginator.page(paginator.num_pages)
            
    context = {'authors': authors,
               'query_tabs': query_tabs,
               'result_title': result_title}
    template = 'crawlers/author-list.html'    

    return render(request, template, context)


@group_required('administrator')
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
        
    context = {'author': author, 'article': article}
    template = "crawlers/dashboard.html"

    return render(request, template, context)