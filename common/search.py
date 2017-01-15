"""
To implement search related queries
Source: http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
"""
from django.db.models import Q
import re
import os, sys, traceback

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    try:
        ret = [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))
        ret = []
                
    return ret 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''    
    query = None # Query to search for every search term
    
    try:        
        terms = normalize_query(query_string)
        for term in terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))            
            
    return query


def get_query_for_nterms(normalized_terms, search_fields):
    '''
    It accept list of normalized terms/tokens, otherwise it is same as 
    `get_query` function.
    Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term
    
    try:
        for term in normalized_terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))            
            
    return query