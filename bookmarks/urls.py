from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^add/?$', views.add_bookmark, name='add-bookmark'),
    url(r'^remove/?$', views.remove_bookmark, name='remove-bookmark'),
    url(r'^list/?$', views.list_bookmark, name='list-bookmark'),
    
]