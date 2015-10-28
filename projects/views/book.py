from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.contrib import messages
from projects.models import Book
from projects.forms import BookForm
from projects import utils
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
#import json

# Create your views here.


def book_details(request, slug, pk):    
    """
    Details of the Book
    """    
    
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Book, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly
    

    
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL

    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    ##
    # Make the context and render
        
    context = {'book': obj}
    template = 'projects/book-details.html'
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)


def book_page_details(request, pk, page_num):
    pass



def book_list(request):
    """
    List view of Book
    """    
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly
    q = request.GET.get('q', None)    
    filters = request.GET.get('filters', None)
    
    if filters:
        filters = filters.split(',')        
        # Supported filters are: 
        pass

    if q:
        q = q.strip()      
        # get the book with 'title'        
        q_objects &= Q(name__icontains=q)      
                
    # Get all authors           
    obj_list = Book.objects.all().filter(q_objects)
    
    ##
    # Check for permissions and render the list of books
    
    
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
            
    context = {'books': objs}
    template = 'projects/book-list.html'    

    return render(request, template, context)