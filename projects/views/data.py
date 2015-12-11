from django.shortcuts import render, get_object_or_404, redirect
import os, sys, traceback
from django.http import HttpResponse
from django.template.context_processors import request
from django.contrib import messages
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from projects.helper import archives, uploads
from projects.forms import UploadScannedImageForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
#import json

# Create your views here.

@login_required
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
    
@login_required
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
        

@login_required
def data_ocr_details(request, pk):
    """
    Project's OCR data (i.e. ) access view
    """
    pass
