from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import os, sys, traceback
from meta_tags.views import Meta
from snippets.models import Snippet
from projects.models import Author
from snippets.forms import SnippetForm
from common.utils import truncatewords, truncatelines
from django.core import serializers
import json

# Create your views here.

def snippet_details(request, pk):
    """
    Details of the Snippet
    """
        
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Snippet, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly
    if request.GET.get('edit', False):
        ##
        # Check for permissions and redirect to AddAuthor view for editing
        
        print "DBG:: Redirecting to edit URL"
        return redirect('snippets:add', pk=obj.id)
    
   
    # Instantiate the Meta class
    title_for_meta = obj.get_title() + ' by ' + obj.author.get_name()    
    meta = Meta(title = title_for_meta, 
                description = truncatelines(obj.body, 4), 
                section= 'poetry', 
                url = obj.get_absolute_url(),                
                author = obj.author, 
                date_time = obj.updated_at,
                object_type = 'article',
                keywords = obj.tags.names(),
            )
    
    ##
    # Make the context and render
  
    context = {'snippet': obj, 'meta': meta}
    template = 'snippets/view.html'
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)    

      
#@login_required   
class AddSnippet(View):
    """
    Add a new Snippet or edit an existing one
    """
    form_class = SnippetForm
    template_name = 'snippets/add-snippet.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
       
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(self.request.user)
        return HttpResponseRedirect(obj.get_absolute_url()) 
    
    def get(self, request, *args, **kwargs):
        if len(kwargs.get('pk', None)) is 0:
            # Create
            form = self.form_class(initial=None)
        else:
            # Update
            self.obj = get_object_or_404(Snippet, pk=kwargs.get('pk', None))
            form = self.form_class(instance=self.obj)
        
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if len(kwargs.get('pk', None)) is not 0:
            # Update
            snippet = Snippet.objects.get(id=kwargs.get('pk', None))
        else:
            # Create
            snippet = Snippet()
            
        form = self.form_class(request.POST, request.FILES, instance=snippet)
        
        if form.is_valid():          
            obj = form.save(self.request.user, commit=False)
            
            if obj.pk:          
                obj.updated_by = self.request.user
            else:
                obj.added_by = self.request.user
                obj.updated_by = self.request.user
            
            obj.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()                
                 
            messages.success(request, 'Changes on snippet "%s" is successful! '%obj.title)        
            return HttpResponseRedirect(obj.get_absolute_url())
        
        return render(request, self.template_name, {'form': form})    

@login_required
def snippet_list(request):
    """
    List Snippet
    """    
    q_objects = Q()
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    author = request.GET.get('author', None)
    q = request.GET.get('q', None)
    filters = request.GET.get('filters', None)
    view = request.GET.get('view', None)
    
    # Default view type is CARD view
    view_type = 'card'
    if view == 't':        
        view_type = 'table'
    #elif view == 'c':
    #    view_type = 'card'    
    
    if filters:
        filters = filters.split(',')
        print filters
        # Supported filters are: pub(published), unpub(unpublished)
        if 'pub' in filters:
            q_objects &= Q(published=True)
        elif 'unpub' in filters:
            q_objects &= Q(published=False)        
        
    if author:
        author = author.strip()
        # filter the source_url
        q_objects &= Q(author__icontains=author)
    
    if q:
        q = q.strip()
        # TODO make it more perfect 
        q_objects &= Q(title__icontains=q) | Q(author__icontains=q)      
        
    # Get all articles              
    obj_list = Snippet.objects.all().filter(q_objects)
       
    ##
    # Check for permissions and render the list of articles
    
    
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
            
    context = {'snippets': objs, 'view': view_type}
    template = 'snippets/snippet-list.html'    

    return render(request, template, context)


def recent_snippets_by_author(request, pk):
    """
    View 10 recent snippets by this Author
    """
    
    # Get the object from the `pk`, raises a Http404 if not found
    author = get_object_or_404(Author, pk=pk)
    
    # Get the articles              
    objs = list(Snippet.objects.filter(author=pk).order_by('-updated_at')[:5])
      
    if request.is_ajax():
        result = []
        for obj in objs:
            data = {}
            data['title'] = obj.title
            data['body'] = obj.get_description()
            data['url'] = obj.get_absolute_url()
            result.append(data)
            
        #serialized_objs = serializers.serialize('json', objs, fields=('title','body', 'get_absolute_url'))

        return HttpResponse(json.dumps(result), content_type="application/json")
    
    context = {'snippets': objs, 'view': 'card'}
    template = 'snippets/snippet-list.html'    

    return render(request, template, context)    
    

def tagged_list(request, slug):
    """
    Views the list of Snippets tagged using 'slug'
    TODO:: Order the list using certain criteria
    """
    try:
        obj_list = Snippet.objects.filter(tags__slug=slug)
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
            
    context = {'snippets': objs, 'tag': slug}
    template = 'snippets/tagged-list.html'    

    return render(request, template, context)


@login_required
def tag_list(request):
    """
    Views the list of all tags
    """
    objs = Snippet.objects.filter(tags__slug=slug)
    context = {'tags': objs}
    template = 'snippets/tag-list.html'    

    return render(request, template, context)


@login_required
def dashboard(request):
    snippet = {}
    snippet['total'] = Snippet.objects.all().count()
    snippet['published'] = Snippet.objects.all().filter(published=True).count()
        
    context = {'snippet': snippet,}
    template = "snippets/dashboard.html"

    return render(request, template, context)