from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from meta_tags.views import Meta
from snippets.models import Snippet
from snippets.forms import SnippetForm
from snippets.utils import truncatewords

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
                description = truncatewords(obj.body, 120), 
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
    template_name = 'snippets/add.html'
    
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
            
    context = {'snippets': objs}
    template = 'snippets/snippet-list.html'    

    return render(request, template, context)


def tagged_list(request, slug):
    """
    Views the list of Snippets tagged using 'slug'
    """
    obj_list = Snippet.objects.filter(tags__slug=slug)
    
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
            
    context = {'snippets': objs}
    template = 'snippets/tagged-list.html'    

    return render(request, template, context)


def tag_list(request):
    """
    Views the list of all tags
    """
    objs = Snippet.objects.filter(tags__slug=slug)
    context = {'tags': objs}
    template = 'snippets/tag-list.html'    

    return render(request, template, context)

def dashboard(request):
    snippet = {}
    snippet['total'] = Snippet.objects.all().count()
    snippet['published'] = Snippet.objects.all().filter(published=True).count()
        
    context = {'snippet': snippet,}
    template = "snippets/dashboard.html"

    return render(request, template, context)