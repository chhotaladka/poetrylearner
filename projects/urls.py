from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^book/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.book_details, name='book-details'),
    url(r'^author/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.author_details, name='author-details'),
    url(r'^project/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.project_details, name='project-details'),
    url(r'^project/data/(?P<pk>\d+)/?$', views.project_data, name='project-data'),
    url(r'^project/?$', views.project_list, name='project-list'),
    
    url(r'^add/author/(?P<pk>\d*)/?$', views.AddAuthor.as_view(), name='add-author'),   
    # For project and book creation and update
    url(r'^add/project/(?P<pk>\d*)/?$', views.AddProjectWizard.as_view(views.PROJECT_FORMS), name='add-project'),
    
    ## Project Data Access ##
    # To add/edit/view scanned pages of a book(i.e. project) 
    url(r'^data/image/(?P<pk>\d*)/?$', views.data_image_details, name='data_image'),
    
    # To view scanned pages' OCR data of a book(i.e. project) 
    url(r'^data/ocr/(?P<pk>\d*)/?$', views.data_ocr_details, name='data_ocr'),
    
]