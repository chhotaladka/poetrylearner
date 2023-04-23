from django.urls import re_path

from . import views

app_name = 'repository'
urlpatterns = [
        
    re_path(r'^add/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)?/?$', views.writers.AddItem.as_view(), name='add-item'),
    re_path(r'^add/?$', views.writers.add, name='add'),
    
    re_path(r'^data/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/publish/?$', views.writers.publish, name='publish'),
    
    re_path(r'^data/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.readers.item, name='item'),
    re_path(r'^data/(?P<item_type>[\w.@+-]+)/?$', views.readers.item_list, name='list'),
    re_path(r'^data/?$', views.readers.items, name='view'),

    re_path(r'^poetry/tag/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'item_type': 'poetry'}, name='tagged-poetry'),
    re_path(r'^snippet/tag/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'item_type': 'snippet'}, name='tagged-snippet'),

    re_path(r'^search/person/?$', views.search.person, name='search-person'),
    re_path(r'^search/org/?$', views.search.organization, name='search-organization'),
    
    re_path(r'^ajax/poetry/?$', views.ajax.poetry_related, name='ajax-poetry-related'),
    
    re_path(r'^$', views.readers.home, name='home'),
    
]
