from django.shortcuts import render, get_object_or_404
import sys, traceback
from django.contrib.auth.decorators import login_required
import random

from repository.models import Poetry, Person
from common.decorators import group_required


def get_random_poetry(creator_id=None, published=False):
    '''
    Get a random Poetry
    '''
    kwargs = {}
    
    if creator_id:
        kwargs['creator'] = creator_id
    
    if published:
        kwargs['published'] = True
    else:
        kwargs['published'] = False
    
    count = Poetry.objects.apply_filter(**kwargs).count()
    
    if count:  
        try:
            index = random.randint(0, count-1)
            obj = Poetry.objects.apply_filter(**kwargs)[index]
        except:
            print ("Error: get_random_poetry: count", count)
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))
            obj = {}
    else:
        obj = {}
           
    return obj

@login_required 
@group_required('administrator', 'editor')
def home(request, src=None):
    '''
    Home page for proofreader
    '''
    context = {'obj': None }
    template = 'proofreader/home.html'
    return render(request, template, context)


@login_required 
@group_required('administrator', 'editor')
def proofread_poetry(request, pk=None, src=None):
    '''
    @summary: Serve an item (Poetry) for proofreading by the Editors
    
    @scope: private
    '''
    result_title = 'Proofreading Poetry'
    
    # Get the object from the `pk`, raises a Http404 if not found
    if pk is None:
        ##
        # Check the parameters passed in the URL and process accordingly
        # Creator_id
        creator_id = None
        poet = request.GET.get('poet', None)
        if poet:
            try:
                creator = get_object_or_404(Person, pk=int(poet))
                result_title = 'Proofreading poetry of ' + creator.popular_name()
                creator_id = creator.id
            except (TypeError, ValueError):
                print 'Error: proofread: poet is not an integer, pass silently'
        
        obj = get_random_poetry(creator_id=creator_id, published=False)
    
    else:
        obj = get_object_or_404(Poetry, pk=pk)
    
    context = {'obj': obj,
               'item_type': 'poetry',
               'result_title': result_title,
               'src': src}
    template = 'proofreader/poetry.html'
    return render(request, template, context)


