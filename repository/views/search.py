from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.decorators import method_decorator
import json
from repository.models import *
from common.search import get_query, normalize_query, get_query_for_nterms

# Create your views here.

def search_person(query_string):
    '''
    Process the query_string and return the `Person` object list
    '''
    
    terms = normalize_query(query_string)
    if (len(terms) == 1): # If only one token
        if (len(terms[0]) == 1): # If it's length is ONE
            if terms[0].isalpha(): # If it is alphabet
                # return the Person whose name starts with `query_string`
                q_objects = Q(name__istartswith=terms[0])
                q_objects |= Q(additional_name__istartswith=terms[0])
                #print q_objects
                obj_list = Person.objects.filter(q_objects).order_by('name')
                return obj_list
            else:
                # Search is irrelevant; return empty list
                return []
        elif len(terms[0]) < 3:
            # Search in name/additional_name fields only
            q_objects = Q(name__icontains=terms[0])
            q_objects |= Q(additional_name__icontains=terms[0])
            #print q_objects
            obj_list = Person.objects.filter(q_objects).order_by('name')
            return obj_list
    
    # We are here, it means:
    # 1) There are multiple terms, or
    # 2) There is single term with length >= 3
    # Now discard all term with length < 3
    terms_n = []
    for term in terms:
        if len(term) < 3:
            pass
        else:
            terms_n.append(term)
    
    entry_query = get_query_for_nterms(terms_n, ['name', 'additional_name', 'description'])
    #print entry_query
    obj_list = Person.objects.filter(entry_query).order_by('name')
    return obj_list


def person(request):
    '''
    For ajax search of `Person` select field
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
        data['additional_name'] = obj.additional_name
        data['birth'] = obj.year_birth if obj.year_birth else ''
        data['death'] = obj.year_death if obj.year_death else ''
        data['url'] = obj.get_absolute_url()
        result.append(data)
        
    r = json.dumps(result)
                  
    return HttpResponse(r, content_type="application/json")


def organization(request):
    '''
    For ajax search of `Organization` select field
    '''
    # Search query
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name',])
        obj_list = Organization.objects.filter(entry_query).order_by('name')[:5]
    else:
        obj_list = []
            
    result = []
    for obj in obj_list:
        data = {}
        data['id'] = obj.id
        data['name'] = obj.name
        data['url'] = obj.get_absolute_url()
        result.append(data)
        
    r = json.dumps(result)
                  
    return HttpResponse(r, content_type="application/json")