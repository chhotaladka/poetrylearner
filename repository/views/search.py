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
from common.search import get_query, normalize_query, get_query_for_nterms, strip_stopwords

# Create your views here.

def search_person(query_string):
    '''
    Process the query_string and return the `Person` object list
    '''
    
    terms = normalize_query(query_string)
    
    if len(terms) == 0:
        # There are no terms
        return []
    
    if len(terms) == 1:
        # There is only ONE term of any length
        # Process the term
        token = terms[0]
    
    else:
        # Keep terms having valid length
        # Discard all term with length < 3
        terms1 = [x for x in terms if len(x) >= 3 ]
    
        if len(terms1) == 0:
            # There are no terms of valid length
            # e.g. "ab cd ef", "a bc de", "a b c", "a b", "ab cd" etc.
            # Process first term and discard others
            token = terms[0]
        
        elif len(terms1) == 1:
            # There are only ONE term of valid length
            # e.g. "abc", "abcd" etc.
            token = terms1[0]
        else:
            token = ''
    
    
    if len(token):
        # Process the token
        if (len(token) == 1): # If it's length is ONE
            if token.isalpha(): # If it is alphabet
                # return the Person whose name starts with `query_string`
                q_objects = Q(name__istartswith=token)
                q_objects |= Q(additional_name__istartswith=token)
                #print q_objects
                obj_list = Person.objects.filter(q_objects).order_by('name')
                return obj_list
            else:
                # Search is irrelevant; return empty list
                return []
            
        elif (len(token) <= 3):
            # Search in name/additional_name fields only
            q_objects = Q(name__icontains=token)
            q_objects |= Q(additional_name__icontains=token)
            #print q_objects
            obj_list = Person.objects.filter(q_objects).order_by('name')
            return obj_list
    
    
    # We are here, it means:
    # 1) There are multiple terms of valid length (>3)
    # First search in `name`/`additional_name` fields
    entry_query1 = get_query_for_nterms(terms1, ['name', 'additional_name'])
    
    # Now remove the STOP WORDS such as A, THE, AND etc
    # and search in `description` field
    terms2 = strip_stopwords(terms1)
    if len(terms2):
        entry_query2 = get_query_for_nterms(terms2, ['description'])
    else:
        entry_query2 = Q()
    
    # Run the query
    q = entry_query1 | entry_query2
    obj_list = Person.objects.filter(q)
    
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