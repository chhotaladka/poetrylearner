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
from django.conf.global_settings import LANGUAGES
import json
import random

from repository.models import Poetry, Person

from common.search import get_query
from common.utils import user_has_group
from meta_tags.views import Meta

# Create your views here.

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


def poetry_related(request, src=None):
    '''
    @summary: Returns related poetry mix
    
    @src: Source of access. It is being used to manipulate the context/templates.
        eg. src='public_url' means this view is being accessed using some public url.
    '''
    if request.is_ajax() is False:
        raise PermissionDenied
    
    ##
    # Check the parameters passed in the URL and process accordingly
    id = request.GET.get('id', 320)
    #mix = request.GET.get('mix', 'related')
    
    mix1_count = 5 # Creator's random poetry
    mix2_count = 5 # Other random poetry
    mix3_count = 5 # Related poetry based on tags(keywords)
    
    try:
        ref_poetry = Poetry.objects.get(pk=id)
    except Poetry.DoesNotExist:
        print "ERR:: The content of object doesn't exist"
        data = {}
        data['status'] = 404
        data['contenthtml'] = ''
        return JsonResponse(data)
    
    # Select `mix1_count` random poetry by creator of `ref_poetry`
    q_objects = Q()
    q_objects &= Q(date_published__isnull=False)
    q_objects &= Q(creator_id=ref_poetry.creator_id)
    
    id_list = Poetry.objects.filter(q_objects).values_list('id', flat=True)
    count = len(id_list)
    mix1_count = mix1_count if count > mix1_count else count
    mix1_ids = random.sample(id_list, mix1_count)
    
    # Select `mix2_count` random poetry by other creators
    q_objects = Q()
    q_objects &= Q(date_published__isnull=False)
    q_objects &= ~Q(creator_id=ref_poetry.creator_id)
    id_list = Poetry.objects.filter(q_objects).values_list('id', flat=True)
    count = len(id_list)
    mix2_count = mix2_count if count > mix2_count else counts
    mix2_ids = random.sample(id_list, mix2_count)
    
    ids = mix1_ids + mix2_ids
    obj_list = Poetry.objects.filter(id__in=ids)
    
    data = {}
    data['status'] = 200
    data['contenthtml'] = render_to_string("repository/include/list/poetry-ajax.html",
                                            {'items': obj_list})
    
    return JsonResponse(data)

