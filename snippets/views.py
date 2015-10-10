from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.base import View

from snippets.models import Snippet
from snippets.forms import SnippetForm

# Create your views here.

def snippet_details(request, slug, pk):
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
    
    ##
    # Check, if `slug` is different from what it is expected,
    # soft-redirect to the correct URL
    
    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    
    ##
    # Make the context and render
  
    context = {'snippet': obj,}
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
            obj = form.save(self.request.user, commit=True)    
            messages.success(request, 'Changes on snippet %s is successful! '%obj.title)        
            return HttpResponseRedirect(obj.get_absolute_url())
        
        return render(request, self.template_name, {'form': form})    
