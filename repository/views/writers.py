from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
import json

from repository.models import *
from repository.forms import *


class CreateThingView(View):
    '''
    Add/Edit an Item(Thing)
    '''
    model = Person
    form_class = PersonForm
    template_name = 'repository/add-person.html'
    ajax_template_name = 'repository/include/form-person.html'
    cancel_url = '/'    
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(self.request.user)
        return HttpResponseRedirect(obj.get_absolute_url()) 
    
    #@login_required(function, redirect_field_name, login_url)
    def get(self, request, *args, **kwargs):
        # Check the parameters passed in the URL and process accordingly
        # Prepare the cancel_url for 'Cancel button' to be passed with the context    
        self.cancel_url = request.GET.get('cancel', '/') 
        
        if request.is_ajax():
            self.template_name = self.ajax_template_name
            
        if len(kwargs.get('pk', None)) is 0:
            # Create
            form = self.form_class(initial=None)
        else:
            # Update
            self.obj = get_object_or_404(self.model, pk=kwargs.get('pk', None))
            form = self.form_class(instance=self.obj)

        return render(request, self.template_name, {'form': form, 'cancel_url': self.cancel_url})

    def post(self, request, *args, **kwargs):
        print "Post data"
        if request.is_ajax():
            self.template_name = self.ajax_template_name
                    
        if len(kwargs.get('pk', None)) is not 0:
            # Update
            instance = self.model.objects.get(id=kwargs.get('pk', None))
        else:
            # Create
            instance = self.model()
            
        form = self.form_class(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            print "Form is valid"
            try:          
                obj = form.save(self.request.user, commit=False)
                if not obj.pk:          
                    obj.added_by = self.request.user                    
                obj.modified_by = self.request.user                
                obj.save()
                # Without this next line the M2M fields won't be saved.
                form.save_m2m()                  
                        
                if request.is_ajax():
                    # Create JSON response and send
                    res = {}
                    res['result'] = 'success'
                    res['url'] = obj.get_absolute_url()
                    return JsonResponse(res)
                                
                messages.success(request, 'Changes on item %s are successful! '%obj.name)        
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
                        
        return render(request, self.template_name, {'form': form, 'cancel_url': self.cancel_url})


class AddPerson(CreateThingView):
    '''
    Add/Edit a Person
    '''
    model = Person
    form_class = PersonForm
    template_name = 'repository/add-person.html'
    ajax_template_name = 'repository/include/form-person.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    
class AddOrg(CreateThingView):
    '''
    Add/Edit an Organization
    '''
    model = Organization
    form_class = OrganizationForm
    template_name = 'repository/items/add-organization.html'
    ajax_template_name = 'repository/include/form-organization.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
    
class AddPlace(CreateThingView):
    '''
    Add/Edit a Place
    '''
    model = Place
    form_class = PlaceForm
    template_name = 'repository/items/add-place.html'
    ajax_template_name = 'repository/include/form-place.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs) 
    
class AddProduct(CreateThingView):
    '''
    Add/Edit a Product
    '''
    model = Product
    form_class = ProductForm
    template_name = 'repository/items/add-product.html'
    ajax_template_name = 'repository/include/form-product.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
class AddEvent(CreateThingView):
    '''
    Add/Edit a Event
    '''
    model = Event
    form_class = EventForm
    template_name = 'repository/items/add-event.html'
    ajax_template_name = 'repository/include/form-event.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
class AddBook(CreateThingView):
    '''
    Add/Edit a Book
    '''
    model = Book
    form_class = BookForm
    template_name = 'repository/items/add-book.html'
    ajax_template_name = 'repository/include/form-book.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
class AddPoetry(CreateThingView):
    '''
    Add/Edit a Poetry
    '''
    model = Poetry
    form_class = PoetryForm
    template_name = 'repository/items/add-poetry.html'
    ajax_template_name = 'repository/include/form-poetry.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs) 
    
class AddSnippet(CreateThingView):
    '''
    Add/Edit a Snippet
    '''
    model = Snippet
    form_class = SnippetForm
    template_name = 'repository/items/add-snippet.html'
    ajax_template_name = 'repository/include/form-snippet.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)                                           