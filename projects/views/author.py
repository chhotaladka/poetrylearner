from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.views.generic.base import View
from django.contrib import messages
from projects.models import Author
from projects.forms import AuthorForm
from projects import utils
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.decorators import method_decorator
import json
from common.search import get_query

# Create your views here.


def author_details(request, slug, pk):
    """
    Details of the Author
    """
        
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Author, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    if request.GET.get('edit', False):
        # Check for permissions and redirect to AddAuthor view for editing        
        print "DBG:: Redirecting to edit URL"
        return redirect('projects:add-author', pk=obj.id)
    
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL    
    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    ##
    # Make the context and render  
    context = {'author': obj }
    template = "projects/author-details.html"
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)


class AddAuthor(View):
    """
    Add a new Author or Modify the existing
    """
    form_class = AuthorForm
    template_name = 'projects/add-author.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)    
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(self.request.user)
        return HttpResponseRedirect(obj.get_absolute_url()) 
    
    #@login_required(function, redirect_field_name, login_url)
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'projects/include/form-author.html'
            
        if len(kwargs.get('pk', None)) is 0:
            # Create
            form = self.form_class(initial=None)
        else:
            # Update
            self.obj = get_object_or_404(Author, pk=kwargs.get('pk', None))
            form = self.form_class(instance=self.obj)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'projects/include/form-author.html'
                    
        if len(kwargs.get('pk', None)) is not 0:
            # Update
            author = Author.objects.get(id=kwargs.get('pk', None))
        else:
            # Create
            author = Author()
            
        form = self.form_class(request.POST, request.FILES, instance=author)
        
        if form.is_valid():
            try:          
                obj = form.save(self.request.user, commit=True)
                        
                if request.is_ajax():
                    # Create JSON response and send
                    res = {}
                    res['result'] = 'success'
                    res['url'] = obj.get_absolute_url()
                    return JsonResponse(res)

                messages.success(request, 'Changes on author %s is successful! '%obj.name)        
                return HttpResponseRedirect(obj.get_absolute_url())
                            
            except:
                print ("Error: Unexpected error:", sys.exc_info()[0])
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print ("DBG:: Error in %s on line %d" % (fname, lineno))
                # Add non_field_errors to the form to convey the message    
                form.add_error(None, "Unexpected error occured! Checking the fields may help.")                 
                               
        if request.is_ajax():
            # Create JSON response alongwith the rendered form and send
            res = {}
            res['result'] = 'failure'
            res['data'] = render_to_string(self.template_name, {'form': form})                
            return JsonResponse(res)
                        
        return render(request, self.template_name, {'form': form})



def author_list(request):
    """
    List view of Author
    """    
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
            obj_list = Author.objects.all().filter(q_objects).order_by('-name')
        else:
            obj_list = Author.objects.all().filter(q_objects).order_by('name')
    elif sort == 'edit':
        if order == 'inc':
            obj_list = Author.objects.all().filter(q_objects).order_by('date_modified')
        else:
            obj_list = Author.objects.all().filter(q_objects).order_by('-date_modified')    
    else:
        obj_list = Author.objects.all().filter(q_objects)
        
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
            
    context = {'authors': objs, 'view': view_type}
    template = 'projects/author-list.html'    

    return render(request, template, context)


def search_author(request):
    """
    For ajax search of author select field
    """

    # Search query
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name_en', 'name', 'sobriquet',])
        obj_list = Author.objects.filter(entry_query).order_by('name')[:5]
    else:
        obj_list = []
            
    result = []
    for obj in obj_list:
        data = {}
        data['id'] = obj.id
        data['name'] = obj.name
        data['name_en'] = obj.name_en
        data['birth'] = obj.date_birth.year if obj.date_birth else ''
        data['death'] = obj.date_death.year if obj.date_death else ''
        data['url'] = obj.get_absolute_url()
        result.append(data)
        
    r = json.dumps(result)
                  
    return HttpResponse(r, content_type="application/json")    