from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
import os, sys, traceback
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bookmarks.models import Bookmark 

# Create your views here.

@login_required
def add_bookmark(request):
    '''
    Add a bookmark for the user on given object
    '''
    if request.method == "POST":
        content_type_id = request.POST.get('type')
        object_id = request.POST.get('id')
        bookmark_id = 0
        #print "DBG:: bookmark add - content_type_id, object_id :", content_type_id, object_id
        
        # Check input data validity
        try:
            content_type_id = int(content_type_id)
            object_id = int(object_id)
        except ValueError:
            print "ERR:: Invalid content_type_id, object_id :", content_type_id, object_id
            data = {}
            data['status'] = 404
            data['bid'] = bookmark_id
            return JsonResponse(data)

        # Validate content_type_id and object_id
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
            content_object = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            print "ERR:: The content of object doesn't exist"
            data = {}
            data['status'] = 404
            data['bid'] = bookmark_id
            return JsonResponse(data)
        
        # Add bookmark
        obj = Bookmark.objects.add_bookmark(content_object, request.user)
        if obj:
            status = 200 # OK
            bookmark_id = obj.id
        else:
            print "ERR:: add bookmark, content_type_id", content_type_id, "obj", object_id
            status = 500 # Internal server error
            
        data = {}
        data['status'] = status
        data['bid'] = bookmark_id
        
        return JsonResponse(data)
    
    else:
        raise PermissionDenied
    

@login_required
def remove_bookmark(request):
    '''
    Remove the bookmark by the user on given object
    '''
    if request.method == "POST":
        content_type_id = request.POST.get('type')
        object_id = request.POST.get('id')
        #print "DBG:: bookmark remove - content_type_id, object_id :", content_type_id, object_id

        # Check input data validity
        try:
            content_type_id = int(content_type_id)
            object_id = int(object_id)
        except:
            print "ERR:: Invalid content_type_id, object_id :"
            data = {}
            data['status'] = 404
            data['bid'] = 0
            return JsonResponse(data)
        
        # Validate content_type_id and object_id
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
            content_object = content_type.get_object_for_this_type(pk=object_id)
            # Delete bookmark
            id = Bookmark.objects.remove_bookmark(content_object, request.user)
        except ObjectDoesNotExist:
            status = 404
        
        status = 200 # Ok
            
        data = {}
        data['status'] = status
        data['bid'] = 0
        
        return JsonResponse(data)
    
    else:
        raise PermissionDenied


@login_required
def list_bookmarks(request):
    '''
    List all bookmarks by the user
    '''
    poetry_ctype = ContentType.objects.get(app_label="repository", model="poetry")
    
    bookmarks = request.user.saved_bookmarks.filter(content_type=poetry_ctype)
    
    obj_list = [x.content_object for x in bookmarks]
    
    # Pagination
    paginator = Paginator(obj_list, 100) # Show 100 entries per page    
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
    
    type = 'Bookmarks'
    result_title = ''
    
    context = {'items': objs,
               'item_type': type, 'result_title': result_title,
               }
    template = 'bookmarks/list.html'
    return render(request, template, context)


@login_required
def search_bookmarks(request):
    '''
    TODO: Search in the bookmarks
    '''
    pass