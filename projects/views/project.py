from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.contrib import messages
from projects.models import Project, Book, Author
from projects.forms import ProjectForm, BookForm
from formtools.wizard.views import SessionWizardView
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
#import json

# Create your views here.
     

#@login_required
def project_details(request, slug, pk):
    """
    Details of the Project
    """
    
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Project, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    if request.GET.get('edit', False):
        ##
        # Check for permissions and redirect to project add/edit URL
        
        print "DBG:: Redirecting to edit URL"
        return redirect('projects:add-project', pk=obj.id)
    
    if request.GET.get('view', None) == 'data':
        ##
        # Check for permissions and redirect to Project Data page
        
        return redirect('projects:project-data', pk=obj.id)
    
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL
    
    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    ##
    # Make the context and render
        
    context = {'project': obj}
    template = 'projects/project-details.html'
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)


  
PROJECT_FORMS = [("bookform", BookForm),
                 ("projectform", ProjectForm),
                ]
#@login_required   
class AddProjectWizard(SessionWizardView):
    """
    AddProjectWizard
    Accessing Book and Project Froms in single view using `django-formtools`
    Reference: https://django-formtools.readthedocs.org/en/latest/wizard.html
    Template: Reference#creating-templates-for-the-forms
    """  
    
    template_name = 'projects/add-project.html'
    book_instance = None
    project_instance = None
       
    def get_form_initial(self, step):

        pk = self.kwargs.get('pk', None)
        if len(pk) is not 0:
            project = get_object_or_404(Project, pk=pk)
            
            ##
            # Make sure the project is in 'INITIATION' state
            # Changes can not be done when its state is other than 'INITIATION'
            
            if project.state != 1:
                #messages.warning(request, 'You can not modify the project in its current state')
                print "DBG:: Project can not be modified in state: ", project.get_state_name()
                raise PermissionDenied()
        
            if step == 'bookform':
                book = project.book            
                book_dict = model_to_dict(book)
                return book_dict
            elif step == 'projectform':
                #project_dict = model_to_dict(project, fields, exclude)
                project_dict = model_to_dict(project)
                return project_dict
        else:    
            return self.initial_dict.get(step, {})
    
    def get_form_instance(self, step):
                           
        if self.book_instance is None or self.project_instance is None:

            pk = self.kwargs.get('pk', None)
            if pk:
                print "DBG:: init for Edit instances", step
                project = get_object_or_404(Project, pk=pk)
                if step == 'bookform':
                    self.book_instance = project.book
                    print "DBG:: book id: ", self.book_instance.id
                    return self.book_instance
                elif step == 'projectform':
                    self.project_instance = project
                    print "DBG:: project id: ", self.project_instance.id
                    return self.project_instance
            else:
                print "DBG:: init for Create new Instances", step
                if step == 'bookform':
                    self.book_instance = Book()
                    return self.book_instance
                elif step == 'projectform':
                    self.project_instance = Project()
                    return self.project_instance    
        else:
            print "DBG:: return existing instances", step
            if step == 'bookform':  
                return self.book_instance
            elif step == 'projectform':
                return self.project_instance        
        
    
    def done(self, form_list, **kwargs):
        """
        Save info to the DB
        """
        print "DBG:: AddProjectWizard done"
        
        book = form_list[0]
        project = form_list[1]
           
        if book.instance.id is None:
            # Create a new book and assign to project
            print "DBG:: Create a new book"
            project.instance.book = book.save(self.request.user)
        else:
            # Update the existing book
            print "DBG:: Update the existing book"
            book.save(self.request.user)
             
        obj = project.save(self.request.user)
        
        ##
        # Update some important fields of `Book.authors.modified_by` in case the 
        # Author was created while creating the project/book with the help of some widget.        
        for author in obj.book.authors.all():
            if author.modified_by is None:
                # It means it is new entry
                print "DBG:: updating info for the new author ", author.name
                author.modified_by = self.request.user
                author.save()
                
        messages.success(self.request, 'Changes on project %s is successful! '%obj.book.name)
        return HttpResponseRedirect(obj.get_absolute_url())


def project_list(request):
    """
    List view of Project
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
        q_objects &= Q(book_name__icontains=q)      
                
    # Get all authors           
    obj_list = Project.objects.all().filter(q_objects)
    
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
            
    context = {'projects': objs}
    template = 'projects/project-list.html'    

    return render(request, template, context)


def dashboard(request):
    project = {}
    book = {}
    author = {}
    
    author['total'] = Author.objects.all().count
    book['total'] = Book.objects.all().count
    project['total'] = Project.objects.all().count     
        
    context = {'author': author, 'book': book, 'project': project}
    template = "projects/dashboard.html"

    return render(request, template, context)