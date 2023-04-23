from django.urls import re_path

from . import views

app_name = 'bookmarks'
urlpatterns = [
    
    re_path(r'^add/?$', views.add_bookmark, name='add-bookmark'),
    re_path(r'^remove/?$', views.remove_bookmark, name='remove-bookmark'),
    re_path(r'^$', views.list_bookmarks, name='list-bookmarks'),
    
]
