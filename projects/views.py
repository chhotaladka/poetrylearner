from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.views.generic.base import View
from django.contrib import messages
from projects.models import Project, Book, Author
from projects.forms import ProjectForm, BookForm, AuthorForm
from projects import utils
from formtools.wizard.views import SessionWizardView
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from projects.helper import archives, uploads
from projects.forms import UploadScannedImageForm
from django.http import JsonResponse
from django.template.loader import render_to_string
#import json

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
        ##
        # Check for permissions and redirect to AddAuthor view for editing
        
        print "DBG:: Redirecting to edit URL"
        return redirect('projects:add-author', pk=obj.id)
    
    ##
    # Check, if `slug` is different from what it is expected,
    # softredirect to the correct URL
    
    if slug != obj.get_slug():
        print "DBG:: Redirecting to correct URL"
        return redirect(obj)
    
    
    url = obj.source_url
    # If url has value, then fetch info from the url
    fetched_info = {}
    if url:
        fetched_info = utils.fetch(url)
    
    ##
    # Make the context and render
  
    context = {'author': obj, 'info': fetched_info}
    template = "projects/author-details.html"
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)



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


#@login_required
def project_list(request):    
    """
    List of all Projects
    """    
    
    # Get the object from the `pk`, raises a Http404 if not found
    obj = get_object_or_404(Project, pk=1)
    
    
    ##
    # Make the context and render
        
    context = {'project': obj}
    template = 'projects/project-list.html'
    
    #return render_to_response(template, context , context_instance=RequestContext(request))
    return render(request, template, context)
     

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


#@login_required
def project_data(request, pk):
    """
    Details of Project Data i.e. scanned images, OCR etc
    """    
    
    # Get the object from the `pk`, raises a Http404 if not found    
    obj = get_object_or_404(Project, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    page_num = request.GET.get('page_num', None)
    
    if page_num is not None:
        if request.GET.get('edit', False):
            ##
            # Check for permissions and redirect to add/edit URL
            
            print "DBG:: page edit ", page_num
            #return redirect('projects:add-project', pk=obj.id)
        else:
            # Display the page
            print "DBG: page ", page_num
            pass
    
    if 1:
        ##
        # Check for permissions and render the list of scanned images page
        
        # Get the page numbers of available scanned pages
        filename = obj.get_path_img_scanned()        
        scanned_pages = archives.get_available_pages(filename)
        
        # Pagination
        paginator = Paginator(obj.get_pages(), 100) # Show 100 book's page images per page    
        page = request.GET.get('page')
        try:
            book_pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            book_pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            book_pages = paginator.page(paginator.num_pages)
                
        context = {'project': obj, 'scanned_pages': scanned_pages, 'book_pages': book_pages}
        template = 'projects/project-data.html'
        return render(request, template, context)
    

def data_image_details(request, pk):
    """
    Project's image data (i.e. scanned image and processed image) access view
    """
    
    # Get the object from the `pk`, raises a Http404 if not found    
    obj = get_object_or_404(Project, pk=pk)
    
    ##
    # Check the parameters passed in the URL and process accordingly    
    action = request.GET.get('action', None)
    page = request.GET.get('page', 1) # default page number is first page i.e. 1

    # Convert page to integer
    try: 
        page = int(page)
    except (ValueError):
        # Set default page number to first page i.e. 1
        page = 1

    # Proccess according to the value passed in `action`
    if action == 'add':
        ##
        # Add scanned image for new `page` for Project `obj`
        
        print "DBG:: data_image_details: action=add, project", obj.id, "page", page
        
        template_name = 'projects/data-image-upload.html'    
        json_response = {}       
        
        if request.method == 'POST':
            
            form = UploadScannedImageForm(request.POST, request.FILES)
            
            if form.is_valid():
                # Construct the image name and destination path
                dest = obj.get_path_img_scanned()                    
                
                filename = request.FILES['image'].name               
                file_type = filename.split('.')[-1]
                
                name = '{id}_{p}.{t}'.format(id=obj.id, p='%08d'%(page,), t=file_type)
                                
                ret = uploads.handle_uploaded_scanned_image(request.FILES['image'], dest, name)    
                if ret: # Internal error
                    print 'ERROR:: Oops!! failed to add scanned image for page', page
                    json_response['result'] = 'error'
                                       
                else: # Success
                    ##
                    # Scanned image added. Now do the followings:
                    # 1) Convert to JP2 format and save
                    # 2) Generate OCR data
                    # 3) Response to client
                    
                    #print 'Scanned image for page %d has been added successfully! '%page_num
                    json_response['result'] = 'success'
                                  
            else:
                print "ERROR:: Oops!! form is not valid"
                json_response['result'] = 'failure' # form validation failed                        
            
            # Return JSON resonse  
            print json_response
            return JsonResponse(json_response)
            #return HttpResponse(json.dumps(json_response), content_type="application/json")
        
        else:
            form = UploadScannedImageForm()
            return render(request, template_name, {'form': form})
        
    elif action == 'view':
        ##
        # View scanned image for the `page` of Project `obj`
        # Display jp2 converted image which is most suitable for web display
        
        print "DBG:: data_image_details: action=view, project", obj.id, "page", page
        
        template_name = 'projects/data-image-view.html'
        
        return render(request, template_name, {'xyz': 123})
    
    else:
        template_name = 'projects/data-image-view.html'        
        return render(request, template_name, {'xyz': 123})
        


def data_ocr_details(request, pk):
    """
    Project's OCR data (i.e. ) access view
    """
    pass


#@login_required
class AddAuthor(View):
    """
    Add a new Author or Modify the existing
    """
    form_class = AuthorForm
    template_name = 'projects/add-author.html'
    
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
            obj = form.save(self.request.user, commit=True)
            if request.is_ajax():
                # Create JSON response and send
                res = {}
                res['result'] = 'success'
                res['url'] = obj.get_absolute_url()
                return JsonResponse(res)
               
            messages.success(request, 'Changes on author %s is successful! '%obj.name)        
            return HttpResponseRedirect(obj.get_absolute_url())
        try:
            if request.is_ajax():
                # Create JSON response alongwith the rendered form and send
                res = {}
                res['result'] = 'failure'
                res['data'] = render_to_string(self.template_name, {'form': form})                
                return JsonResponse(res)
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))          
                
        return render(request, self.template_name, {'form': form})


  
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
    
