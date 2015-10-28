from django.conf.urls import url

from . import views

urlpatterns = [

    # Dashboard
    url(r'^$', views.dashboard, name='dashboard'),    
    url(r'^book/?$', views.book_list, name='book-list'),
    url(r'^author/?$', views.author_list, name='author-list'),
    url(r'^project/?$', views.project_list, name='project-list'),
        
    url(r'^book/(?P<pk>\d+)/page/(?P<page_num>\d+)/?$', views.book_page_details, name='book-page-details'),
    url(r'^book/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.book_details, name='book-details'),
    
    url(r'^author/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.author_details, name='author-details'),
    url(r'^project/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.project_details, name='project-details'),
    
    url(r'^project/data/(?P<pk>\d+)/?$', views.project_data, name='project-data'),
    
    url(r'^add/author/(?P<pk>\d*)/?$', views.AddAuthor.as_view(), name='add-author'),   
    # For project and book creation and update
    url(r'^add/project/(?P<pk>\d*)/?$', views.AddProjectWizard.as_view(views.PROJECT_FORMS), name='add-project'),
    
    ## Project Data Access ##
    # To add/edit/view scanned pages of a book(i.e. project) 
    url(r'^data/image/(?P<pk>\d*)/?$', views.data_image_details, name='data_image'),
    
    # To view scanned pages' OCR data of a book(i.e. project) 
    url(r'^data/ocr/(?P<pk>\d*)/?$', views.data_ocr_details, name='data_ocr'),    
       
]