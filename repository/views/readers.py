from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.decorators import method_decorator
import json

from repository.models import *

from common.search import get_query

# Create your views here.

def _resolve_item_type(type, list=False):
    '''
    Check the type i.e. content_type and retunr the model class and template.
    '''
    item_cls = None
    template = None
    list_template = None    
    
    if type == Snippet.content_type():
        item_cls = Snippet
        template = "repository/items/snippet.html" 
        list_template = "repository/include/list/snippet.html" 
        
    elif type == Poetry.content_type():
        item_cls = Poetry
        template = "repository/items/poetry.html"
        list_template = "repository/include/list/poetry.html"
        
    elif type == Person.content_type():
        item_cls = Person
        template = "repository/items/person.html"
        list_template = "repository/include/list/person.html"
        
    elif type == Place.content_type():
        item_cls = Place
        template = "repository/items/place.html"
        list_template = "repository/include/list/place.html" 
               
    elif type == Product.content_type():
        item_cls = Product
        template = "repository/items/product.html"
        list_template = "repository/include/list/product.html"
                  
    elif type == Event.content_type():
        item_cls = Event
        template = "repository/items/event.html"
        list_template = "repository/include/list/event.html" 
                 
    elif type == Organization.content_type():
        item_cls = Organization
        template = "repository/items/organization.html"
        list_template = "repository/include/list/organization.html"  

    elif type == Book.content_type():
        item_cls = Book
        template = "repository/items/book.html"
        list_template = "repository/include/list/book.html"                
    
    if list:
        return item_cls, list_template
    
    return item_cls, template    


def item(request, type, pk, slug):
    '''
    Details of an item
    '''
    print "DBG: requested content type > ", type

    item_cls, template = _resolve_item_type(type)    
    if item_cls is None:
        print "Error: content type is not found"
        raise Http404 
                                       
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(item_cls, pk=pk)
        
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL    
    if slug != obj.get_slug():
        return redirect(obj)
    
    ##
    # Make the context and render  
    context = {'obj': obj }    
    return render(request, template, context)


def items(request):
    '''
    Show all data items
    '''    
    ##
    # Make the context and render  
    context = {'obj': None }
    template = "repository/items/data.html"  
    return render(request, template, context) 


def list(request, type):
    '''
    List the Persons
    '''    
    
    item_cls, list_template = _resolve_item_type(type, list=True)    
    if item_cls is None:
        print "Error: content type is not found"
        raise Http404 
        
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    # Search query
    q = request.GET.get('q', None)
    # Filters for the queryset
    filters = request.GET.get('filters', None)
    # Sort the result by: 'name' for `Author.name`, 'edit' for `Author.date_modified`
    # Default is 'edit' i.e. Give recently edited item first
    sort = request.GET.get('sort', 'edit')
    # Order the result: 'inc' for increasing order; 'dec' for decreasing order
    # Default is 'dec'
    order = request.GET.get('order', 'dec')
    # View type of the result list: 't' for table view; 'c' for card view
    # Default view type is CARD view
    view = request.GET.get('view', 'c')
    
    # Set the view type
    if view == 't':        
        view_type = 'table'
    elif view == 'c':
        view_type = 'card'
    
    # Filter the queryset on the basis of `filters` given
    if filters:
        filters = filters.split(',')        
        # Supported filters are: birth or nobirth, death or nodeath
        if 'birth' in filters:
            # get the authors whom birth info is known
            q_objects &= ~Q(date_birth=None)
        elif 'nobirth' in filters:
            # get the authors whom birth info is not known
            q_objects &= Q(date_birth=None)
        if 'death' in filters:
            # get the authors whom death info is known
            q_objects &= ~Q(date_death=None)
        elif 'nodeath' in filters:
            # get the authors whom death info is not known
            q_objects &= Q(date_death=None)            
    
    # Apply Search query
    if q:
        q = q.strip()      
        # get the authors with 'name'        
        q_objects &= Q(name_en__icontains=q) | Q(name__icontains=q) | Q(sobriquet__icontains=q)      
                
    # Get all authors sorted and ordered
    if sort == 'name':
        if order == 'inc':
            obj_list = item_cls.objects.all().filter(q_objects).order_by('-name')
        else:
            obj_list = item_cls.objects.all().filter(q_objects).order_by('name')
    elif sort == 'edit':
        if order == 'inc':
            obj_list = item_cls.objects.all().filter(q_objects).order_by('date_modified')
        else:
            obj_list = item_cls.objects.all().filter(q_objects).order_by('-date_modified')    
    else:
        obj_list = item_cls.objects.all().filter(q_objects)
        
    ##
    # Check for permissions and render the list of authors
    
    
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
            
    context = {'items': objs, 'list_template': list_template}
    template = 'repository/items/list.html'    

    return render(request, template, context)


def tagged_items(request, slug, type):
    """
    Views the list of Items tagged using 'slug'
    TODO:: Order the list using some criteria
    """

    try:
        if type == Snippet.content_type():
            item_cls = Snippet
            list_template = "repository/include/list/snippet.html" 
            
        else:
            item_cls = Poetry
            list_template = "repository/include/list/poetry.html"
            
        obj_list = item_cls.objects.filter(keywords__slug=slug)
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))
        obj_list = []
    
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
            
    context = {'items': objs, 'tag': slug, 'list_template': list_template}
    template = 'repository/items/tagged-list.html'    

    return render(request, template, context)


def search(request):
    '''
    For ajax search of Person select field
    '''

    # Search query
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name', 'additional_name',])
        obj_list = Person.objects.filter(entry_query).order_by('name')[:5]
    else:
        obj_list = []
            
    result = []
    for obj in obj_list:
        data = {}
        data['id'] = obj.id
        data['name'] = obj.name
        data['name_en'] = obj.additional_name#TODO change name_en to additional_name, elswhere in javascripts
        data['birth'] = obj.date_birth.year if obj.date_birth else ''
        data['death'] = obj.date_death.year if obj.date_death else ''
        data['url'] = obj.get_absolute_url()
        result.append(data)
        
    r = json.dumps(result)
                  
    return HttpResponse(r, content_type="application/json")    