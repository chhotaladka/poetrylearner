from django.shortcuts import render, get_object_or_404, redirect
import sys, traceback
from django.http import (
    Http404, HttpResponseRedirect
)
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.conf.global_settings import LANGUAGES
import random
from django.contrib.sites.shortcuts import get_current_site
from repository.models import *
from repository.views.search import search_person

from common.search import get_query
from common.utils import user_has_group
from meta_tags.views import Meta

# Create your views here.

def _create_query_tabs(request_path='/', q_tab=None, extra_get_queries=[]):
    '''
    Return query tab object for poetry
    '''
    get_query = ''.join(extra_get_queries)
    
    # Create tab list and populate
    query_tabs = []    
    
    tab = {
           'name': 'all',
           'help_text': 'All items',
           'url': request_path + '?tab=all' + get_query,
           'css': 'is-active' if q_tab == 'all' or q_tab is None else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'published',
           'help_text': 'Itmes which are published',
           'url': request_path + '?tab=pub' + get_query,
           'css': 'is-active' if q_tab == 'pub' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'unpublished',
           'help_text': 'Itmes which are not published',
           'url': request_path + '?tab=unpub' + get_query,
           'css': 'is-active' if q_tab == 'unpub' else '',
        }
    query_tabs.append(tab)
    
    return query_tabs
        

def _resolve_item_type(type, list=False):
    '''
    Check the type i.e. item_type and retunr the model class and template.
    '''
    item_cls = None
    template = None
    list_template = None    
    
    if type == Snippet.item_type():
        item_cls = Snippet
        template = "repository/items/snippet.html" 
        list_template = "repository/include/list/snippet.html" 
        
    elif type == Poetry.item_type():
        item_cls = Poetry
        template = "repository/items/poetry.html"
        list_template = "repository/include/list/poetry.html"
        
    elif type == Person.item_type():
        item_cls = Person
        template = "repository/items/person.html"
        list_template = "repository/include/list/person.html"
        
    elif type == Place.item_type():
        item_cls = Place
        template = "repository/items/place.html"
        list_template = "repository/include/list/place.html" 
               
    elif type == Product.item_type():
        item_cls = Product
        template = "repository/items/product.html"
        list_template = "repository/include/list/product.html"
                  
    elif type == Event.item_type():
        item_cls = Event
        template = "repository/items/event.html"
        list_template = "repository/include/list/event.html" 
                 
    elif type == Organization.item_type():
        item_cls = Organization
        template = "repository/items/organization.html"
        list_template = "repository/include/list/organization.html"  

    elif type == Book.item_type():
        item_cls = Book
        template = "repository/items/book.html"
        list_template = "repository/include/list/book.html"
    
    if list:
        return item_cls, list_template
    
    return item_cls, template    


def item(request, type, pk, slug, src=None):
    '''
    @summary: Details of an item
    
    @src: Source of access. It may be used to manipulate the context/templates.
        eg. src='public_url' means this view is being accessed using some public url.
    '''
    
    item_cls, template = _resolve_item_type(type)
    if item_cls is None:
        print "Error: content type is not found"
        raise Http404 
    
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(item_cls, pk=pk)
    
    # Check for permissions
    if src != 'public_url':
        # public users should not have access to repository urls '/r/data/...'
        # redirect to respective public url
        if user_has_group(request.user, ['Administrator', 'Editor']) is False:
            return HttpResponseRedirect(obj.get_absolute_url())
    
    if type == 'poetry' or type == 'snippet':
        if user_has_group(request.user, ['Administrator', 'Editor']) is False:
            # Do not show unpublished `poetry`, `snippet` 
            if obj.is_published() is False:
                raise PermissionDenied
    
    # Check, if `slug` is different from what it is expected,
    if slug != obj.get_slug():
        if user_has_group(request.user, ['Administrator', 'Editor']):
            # softredirect to correct url
            return redirect(obj)
        else:
            # softredirect to the item list page
            return HttpResponseRedirect(obj.get_list_url())
    
    # Instantiate the Meta class
    if type == 'poetry':
        meta_image_url = obj.creator.get_image_url()
    elif type == 'person':
        meta_image_url = obj.get_image_url()
    else:
        meta_image_url = "img/poetrylearner_logo_120x120.png"
        
    meta = Meta(title = obj.title(), 
                description = obj.meta_description(), 
                section= type, 
                url = obj.get_absolute_url(),
                author = obj.get_author(), 
                date_time = obj.get_last_edit_time(),
                object_type = 'article',
                keywords = obj.get_keywords(),
                image = meta_image_url,
            )
    
    # Make the context and render  
    context = {'obj': obj, 'meta': meta, 'item_type': type, 
               'src': src}    
    return render(request, template, context)


def home(request):
    '''
    @summary: Show home page of Repository
    @note: Only Administrator & Editor have access (redirect others to home page).
    '''
    if user_has_group(request.user, ['Administrator', 'Editor']) is False:
        # Redirect to home page
        return redirect('/')
    
    else:
        # Make the context and render  
        context = {'obj': None }
        template = "repository/home.html"  
        return render(request, template, context)


def items(request):
    '''
    @summary: Show all data items
    @note: Only Administrator & Editor have access (redirect others to home page).
    '''
    
    if user_has_group(request.user, ['Administrator', 'Editor']) is False:
        # Redirect to home page
        return redirect('/')
    
    else:
        count = {}
        count['poetry'] = Poetry.objects.all().count
        count['snippet'] = Snippet.objects.all().count
        count['person'] = Person.objects.all().count
        count['place'] = Place.objects.all().count
        count['product'] = Product.objects.all().count
        count['event'] = Event.objects.all().count
        count['organization'] = Organization.objects.all().count
        count['book'] = Book.objects.all().count
        
        # Make the context and render  
        context = {'obj': None, 'count': count }
        template = "repository/items/data.html"
        return render(request, template, context)


def list(request, type, src=None):
    '''
    @summary: List the data item of `type`
    
    @src: Source of access. It may be used to manipulate the context/templates.
        eg. src='public_url' means this view is being accessed using some public url.    
    '''    
    
    item_cls, list_template = _resolve_item_type(type, list=True)
    if item_cls is None:
        print "Error: content type is not found"
        raise Http404 
        
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly

    # Query tab
    q_tab = request.GET.get('tab', None)
        
    # Creator id (valid for items derived from `CreativeWork`)
    creator = request.GET.get('creator', None)
    # Language (valid for items derived from `CreativeWork`)
    language = request.GET.get('lan', None)
    # Sort the result by: 'name' for `Author.name`, 'edit' for `Author.date_modified`
    # Default is 'edit' i.e. Give recently edited item first
    sort = request.GET.get('sort', 'edit')
    # Order the result: 
    #    'recent' for recently changed items first;
    #    'random' for random selection;
    #    Default is 'recent'
    order = request.GET.get('o', 'recent')
              
    obj_list = []
    result_title = item_cls._meta.verbose_name_plural.title()
    kwargs = {}
    query_tabs = []
    extra_get_queries = []

    #
    ## Process get queries
    if q_tab:
        if q_tab == 'all':
            pass
        elif q_tab == 'pub':
            kwargs['published'] = True
        elif q_tab == 'unpub':
            kwargs['published'] = False
        else:
            # Set the q_tab to None: ignore other values
            q_tab = None
    
    # Set order to its default i.e. `recent` if it is not the expected one.
    if order != 'shuffle':
        order = 'recent'
    q_string = '&o=' + order
    extra_get_queries.append(q_string)
            
    # Get the items having creator.id = creator
    if creator:
        try:
            q_string = '&creator=' + creator
            extra_get_queries.append(q_string)
            creator = int(creator)
            result_title = get_object_or_404(Person, pk=creator).full_name() 
            kwargs['creator'] = creator

        except (TypeError, ValueError):
            print 'Error: That creator_id is not an integer, pass silently'
            pass

    if language:
        tmp = dict(LANGUAGES)
        if language in tmp:
            q_string = '&lan=' + language
            extra_get_queries.append(q_string)
            kwargs['language'] = language
            result_title += ', #' + tmp[language]

    # Only for ``poetry`` and ``snippet``
    if type == 'poetry' or type == 'snippet':
        # Check for permissions
        if user_has_group(request.user, ['Administrator', 'Editor']):
            # Create ``query_tabs`` for user of Administrator and Editor groups
            query_tabs = _create_query_tabs(request.path, q_tab, extra_get_queries)
        else:
            # Create ``query_tabs`` for public users
            query_tabs = []
            # Show only published `poetry`, `snippet` 
            kwargs['published'] = True
    
    if order == 'shuffle':
        # Note: order_by('?') queries may be expensive and slow, 
        # depending on the database backend you are using.
        # FIXME: It will slow down if table is large. Use some other options.
        obj_list = item_cls.objects.apply_filter(**kwargs).order_by('?')
    else:
        if (q_tab == 'pub') and (type == 'poetry' or type == 'snippet'):
            obj_list = item_cls.objects.apply_filter(**kwargs).order_by('-date_published')
        else:
            obj_list = item_cls.objects.apply_filter(**kwargs).order_by('-date_modified')
    
    
    # Pagination
    paginator = Paginator(obj_list, 20) # Show 20 entries per page    
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
            
    context = {'items': objs, 'list_template': list_template, 
               'item_type': type, 'result_title': result_title,
               'query_tabs': query_tabs, 'order': order,
               'src': src}
    template = 'repository/items/list.html'

    return render(request, template, context)


def explore_poetry(request, poet=None, slug=None, src=None):
    '''
    @summary: Explore and list the poetry 
    
    @scope: public
    '''
    
    if poet:
        creator = get_object_or_404(Person, pk=poet)
    else:
        creator = None

    ##
    # Check the parameters passed in the URL and process accordingly
    # Language
    language = request.GET.get('lan', None)
    query_string = request.GET.get('q', '')
    
    # If creator(poet) is not given
    if creator is None:
        result_title = 'Poetry'
        objs = None
        # Otherthings will be taken care in template (using templatetags/ajax)
        
    # If creator(poet) is given
    else:
        result_title = 'Poetry by ' + creator.popular_name()
        
        kwargs = {}
        kwargs['creator'] = creator
        kwargs['published'] = True # Show only published `poetry`
        obj_list = []
        obj_list = Poetry.objects.apply_filter(**kwargs).order_by('-date_published')
        
        # Pagination
        paginator = Paginator(obj_list, 40) # Show 40 entries per page    
        page = request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objs = paginator.page(paginator.num_pages)
    
    # Instantiate the Meta class
    if creator:
        meta_image_url = creator.get_image_url()
        print meta_image_url
        meta_description = "%s has %s poetry on %s."%(
            creator.full_name(), paginator.count, get_current_site(request).name)
    else:
        meta_image_url = "img/poetrylearner_logo_120x120.png"
        meta_description = "Read and explore more than %s poetry on %s."%(
            Poetry.objects.all().count(), get_current_site(request).name)
    
    meta = Meta(title = result_title, 
                description = meta_description,
                section= 'Poetry',
                object_type = 'article',
                keywords = None,
                image = meta_image_url,
            )
    
    context = {'items': objs, 'creator': creator, 'language': language,
               'item_type': 'poetry', 'result_title': result_title,
               'query_string': query_string,
               'meta': meta,
               'src': src}
    template = 'repository/items/explore_poetry.html'
    return render(request, template, context)


def explore_poets(request, src=None):
    '''
    @summary: Explore and list the poets i.e. person
    
    @scope: public
    '''
    ##
    # Check the parameters passed in the URL and process accordingly

    if ('q' in request.GET) and request.GET['q'].strip():
        # Search Poets for the query `q`
        query_string = request.GET['q']
        result_title = '"' + query_string + '" in Poets'
        obj_list = search_person(query_string)
        
        # Pagination
        paginator = Paginator(obj_list, 20) # Show 40 entries per page    
        page = request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objs = paginator.page(paginator.num_pages)
        
        template = 'repository/items/search_poets.html'
        
    else:
        query_string = ''
        result_title = 'Poets'
        objs = []
        template = 'repository/items/explore_poets.html'
    
    # Instantiate the Meta class
    meta_image_url = "img/poetrylearner_logo_120x120.png"
    meta_description = "Read and explore the poetry of %s great poets on %s."%(
        Person.objects.all().count(), get_current_site(request).name)
    
    meta = Meta(title = result_title, 
                description = meta_description,
                section= 'Poets',
                object_type = 'article',
                keywords = None,
                image = meta_image_url,
            )
    
    context = {'items': objs,
               'item_type': 'person', 'result_title': result_title,
               'query_string': query_string,
               'meta': meta,
               'src': src}
    return render(request, template, context)


def explore_tags(request, slug, src=None):
    '''
    @summary: Explore and list the tagged items
    
    @scope: public
    '''
    pass


def tagged_items(request, slug, type, src=None):
    """
    @summary: Views the list of Items tagged using 'slug'
        TODO:: Order the list using some criteria
    
    @src: Source of access. It may be used to manipulate the context/templates.
        eg. src='public_url' means this view is being accessed using some public url.        
    """
    
    if type == Snippet.item_type():
        item_cls = Snippet
        list_template = "repository/include/list/snippet.html"        
    else:
        # Currently, tagging is supported only on Snippet & Poetry
        item_cls = Poetry
        list_template = "repository/include/list/poetry.html"
    
    try:
        if user_has_group(request.user, ['Administrator', 'Editor']):    
            obj_list = item_cls.objects.filter(keywords__slug=slug)
        else:
            # Show only published `poetry`, `snippet`
            obj_list = item_cls.published.filter(keywords__slug=slug)
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))
        obj_list = []
    
    result_title = '#' + slug
    
    # Pagination
    paginator = Paginator(obj_list, 20) # Show 20 entries per page    
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
            
    context = {'items': objs, 'tag': slug, 'list_template': list_template, 
               'item_type': type, 'result_title': result_title, 
               'src': src}
    template = 'repository/items/tagged-list.html'    

    return render(request, template, context)


def get_a_poetry():
    '''
    Get a random poetry
    '''
    obj_list = Poetry.published.all()
    count = len(obj_list)    
    
    if count:  
        try:
            index = random.randint(0, count-1)
            obj = obj_list[index]
        except:
            print ("count", count)
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))
            obj = {}
    else:
        obj = {}
           
    return obj
