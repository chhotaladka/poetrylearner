from django.conf.urls import url

from . import views

urlpatterns = [
        
    url(r'^add/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)?/?$', views.writers.AddItem.as_view(), name='add-item'),
    url(r'^add/?$', views.writers.add, name='add'),
    
    url(r'^data/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/publish/?$', views.writers.publish, name='publish'),
    
    url(r'^data/(?P<item_type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.readers.item, name='item'),
    url(r'^data/(?P<item_type>[\w.@+-]+)/?$', views.readers.list, name='list'),
    url(r'^data/?$', views.readers.items, name='view'),

    url(r'^poetry/tag/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'item_type': 'poetry'}, name='tagged-poetry'),
    url(r'^snippet/tag/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'item_type': 'snippet'}, name='tagged-snippet'),

    url(r'^search/person/?$', views.search.person, name='search-person'),
    url(r'^search/org/?$', views.search.organization, name='search-organization'),
    
    url(r'^ajax/poetry/?$', views.ajax.poetry_related, name='ajax-poetry-related'),
    
    url(r'^$', views.readers.home, name='home'),
    
]