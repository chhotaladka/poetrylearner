from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.decorators import method_decorator
import json
import random

from repository.models import Poetry, Person

from common.search import get_query
from common.utils import user_has_group

# Create your views here.

def poetry_related(request, src=None):
    '''
    @summary: Returns related poetry mix
    
    @src: Source of access. It is being used to manipulate the context/templates.
        eg. src='public_url' means this view is being accessed using some public url.
    '''
    #if request.is_ajax() is False:
    #    raise PermissionDenied
    
    template = "repository/include/list/poetry.html"
    
    ##
    # Check the parameters passed in the URL and process accordingly
    id = request.GET.get('id', None)
    continuation = request.GET.get('continuation', None)
    #mix = request.GET.get('mix', 'related')
    
    mix1_count = 5 # Creator's random poetry
    mix2_count = 5 # Other random poetry
    mix3_count = 5 # Related poetry based on tags(keywords)
    
    try:
        ref_poetry = Poetry.objects.get(pk=id)
    except:
        print("ERR:: Poetry.DoesNotExist or ValueError for id", id)
        data = {}
        data['status'] = 404
        data['contenthtml'] = ''
        return JsonResponse(data)
    
    # Decode the value of `continuation`
    exclude_ids = []
    if continuation:
        exclude_ids = continuation.split("i")
    
    exclude_ids.append(id)
    
    # Select `mix1_count` random poetry by creator of `ref_poetry`
    q_objects = Q()
    q_objects &= Q(date_published__isnull=False)
    q_objects &= Q(creator_id=ref_poetry.creator_id)
    try:
        q_ids = Poetry.objects.filter(q_objects).exclude(pk__in=exclude_ids).values_list('id', flat=True)
    except:
        # Chances of exceptions.ValueError, in case if exclude_ids has non integer values
        print(("ERROR: ajax.poetry_related: unexpected error 1:", sys.exc_info()[0]))
        id_list = []
    id_list = list(q_ids) # evaluate queryset
    mix1_ids = random.sample(id_list, min(mix1_count, len(id_list)))
    
    # Select `mix2_count` random poetry by other creators
    q_objects = Q()
    q_objects &= Q(date_published__isnull=False)
    q_objects &= ~Q(creator_id=ref_poetry.creator_id)
    q_ids = Poetry.objects.filter(q_objects).values_list('id', flat=True)
    id_list = list(q_ids) # evaluate queryset
    mix2_ids = random.sample(id_list, min(mix2_count, len(id_list)))
    
    ids = mix1_ids + mix2_ids
    q_objs = Poetry.objects.filter(pk__in=ids)
    # Above queryset gives the result sorted by pk, but we dont want this.
    # We want same ordering as in `ids` list
    obj_list = []
    for id in ids:
        for obj in q_objs:
            if id == obj.id:
                obj_list.append(obj)

    # Encode the values into the `continuation`
    if not continuation:
        continuation = "i".join([str(i) for i in ids])
    
    data = {}
    data['status'] = 200
    data['continuation'] = continuation
    data['contenthtml'] = render_to_string(template, 
                                           {'items': obj_list, 'request': request})
            
    return JsonResponse(data)

