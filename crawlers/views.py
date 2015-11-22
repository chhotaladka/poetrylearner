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
from projects.models import Author
from snippets.models import Snippet

# Create your views here.


"""
Details of the RawArticle
"""
@login_required
def raw_article_details(request, pk):
    obj = get_object_or_404(RawArticle, pk=pk)    
        
    context = {'article': obj}
    template = "crawlers/article-details.html"

    return render(request, template, context)

@login_required
def raw_article_list(request):
    """
    
    """    
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    source = request.GET.get('source', None)
    author = request.GET.get('author', None)
    q = request.GET.get('q', None)
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
        source = source.strip()
        # filter the source_url
        q_objects &= Q(source_url__icontains=source)

    if author:
        author = author.strip()
        # filter the source_url
        q_objects &= Q(author__icontains=author)
    
    if q:
        q = q.strip()
        # TODO make it more perfect 
        q_objects &= Q(source_url__icontains=q) | Q(author__icontains=q) | Q(title__icontains=q)      
        
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


@login_required
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


@login_required
def author_add_snippet(request, pk):
    
    #TODO check for the permission: Only admin and users that can access dashboard are allowed 
    if request.is_ajax():
        name = get_object_or_404(RawAuthor, pk=pk).name
        
        try:
            # Get all raw articles by this author(raw :D) which are not valid 
            q_articles = Q()
            q_articles &= Q(author__icontains=name) & Q(valid=False)                
            raw_articles = RawArticle.objects.all().filter(q_articles)              
            
            count = 0
            
            # Get the `Author` object having name='name'
            # Return failure if not found                
            q_authors = Q()
            q_authors &= Q(name__icontains=name)|Q(name_en__icontains=name)
            author = Author.objects.all().filter(q_authors)[0:1][0]
            
            if author:            
                # Add all 'articles' to Snippet with 'author' as author field
                print "Found author", author.get_name(), " in Projects.Author"
                        
                for raw_article in raw_articles:
                    # Create a new snippet              
                    snippet = Snippet()
                    snippet.title = raw_article.title
                    snippet.body = raw_article.content
                    snippet.author = author
                    snippet.added_by = request.user
                    snippet.updated_by = request.user
                    snippet.save()
                    print "Created Snippet : ", snippet.id
                    
                    # Make the raw_article valid
                    raw_article.snippet = snippet
                    raw_article.valid = True
                    raw_article.save()
                    count += 1
                    
                # Return success with number of snippets made
                print "Total", count, "raw articles added in snippets."                        
                res = {}
                res['result'] = 'success'
                res['count'] = count  
                return JsonResponse(res)
    
            else:
                # Return failure, means You have to add the entry of RawAuthor to Author first
                print "No author found as", name, " in Projects.Author"
                
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


@login_required
def raw_author_list(request):
    """
    List view
    """    
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    source = request.GET.get('source', None)
    q = request.GET.get('q', None)    
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
        source = source.strip()  
        # filter with source_url
        q_objects &= Q(source_url__icontains=source)

    if q:
        q = q.strip()      
        # get the authors with 'name'        
        q_objects &= Q(name__icontains=q) | Q(source_url__icontains=q)      
                
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


@login_required
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