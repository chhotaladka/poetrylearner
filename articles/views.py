from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from articles.models import Article
from articles.forms import *
from django.views.generic.base import View
import random

# Create your views here.

"""
Generate a random article
"""
def random_article(request):
    num = Article.objects.count()
    if num > 0:
        random_id = random.randrange(1, num) #TODO randomly generate
    else:
        random_id = 0
    
    #TODO check if meta.is_published=True then render
    article = get_object_or_404(Article, pk=random_id)
    return render(request, 'articles/article-details.html', {'article': article})

"""
Explore the published articles collection
"""
def explore(request):
    random_id = 10 #TODO randomly generate
    article = get_object_or_404(Article, pk=random_id)
    return render(request, 'explore.html', {'article': article})

   
def article_details(request, slug, pk):
    """
    Details of the Article
    """
        
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Article, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    if request.GET.get('edit', False):
        ##
        # Check for permissions and redirect to AddAuthor view for editing
        
        print "DBG:: Redirecting to edit URL"
        return redirect('articles:edit-article', pk=obj.id)
    
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL
    
    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    
    ##
    # Make the context and render
  
    context = {'article': obj,}
    template = 'articles/article-details.html'
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)    
      

#@login_required
class AddArticle(View):
    """
    Add a new Article or Modify the existing
    """
    form_class = ArticleForm
    template_name = 'articles/add-article.html'
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(self.request.user)
        return HttpResponseRedirect(obj.get_absolute_url()) 
    
    #@login_required(function, redirect_field_name, login_url)
    def get(self, request, *args, **kwargs):
        if len(kwargs.get('pk', None)) is 0:
            # Create
            form = self.form_class(initial=None)
        else:
            # Update
            self.obj = get_object_or_404(Article, pk=kwargs.get('pk', None))
            form = self.form_class(instance=self.obj)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if len(kwargs.get('pk', None)) is not 0:
            # Update
            article = Article.objects.get(id=kwargs.get('pk', None))
        else:
            # Create
            article = Article()
            
        form = self.form_class(request.POST, request.FILES, instance=article)
        
        if form.is_valid():          
            obj = form.save(self.request.user, commit=True)    
            messages.success(request, 'Changes on article %s is successful! '%obj.title)        
            return HttpResponseRedirect(obj.get_absolute_url())
        
        return render(request, self.template_name, {'form': form})    

    
"""
Edit and update an existing Article
"""
#@login_required
class EditArticle(View):
    form_class = UpdateArticleForm
    template_name = 'articles/add-article.html'
    
    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Article, pk=kwargs.get('pk', None))
        
        initial = {'title': self.obj.title,
                  'content': self.obj.content,
                  'page_num': self.obj.page_num,
                  'author': self.obj.author,
                  'book': self.obj.book,
                  'is_published': self.obj.meta.is_published,
                  'is_verified': self.obj.meta.is_verified,
                  }
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        article = Article.objects.get(id=kwargs.get('pk', None))
        if form.is_valid():
            obj = form.save(self.request.user, article.id, commit=True)
            return HttpResponseRedirect(obj.get_absolute_url())

        return render(request, self.template_name, {'form': form})        