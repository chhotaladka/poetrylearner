from django.conf.urls import url

from . import views

urlpatterns = [
        
    url(r'^add/(?P<type>[\w.@+-]+)/(?P<pk>\d+)?/?$', views.writers.AddItem.as_view(), name='add-item'),
    url(r'^add/?$', views.writers.add, name='add'),
    
    url(r'^data/(?P<type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/publish/?$', views.writers.publish, name='publish'),
    
    url(r'^data/(?P<type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>.+)?/?$', views.readers.item, name='item'),
    url(r'^data/(?P<type>[\w.@+-]+)/?$', views.readers.list, name='list'),
    url(r'^data/?$', views.readers.items, name='view'),
    
#     url(r'^(?P<pk>\d+)/?$', views.snippet_details, name='view'),
#     url(r'^add/(?P<pk>\d*)/?$', views.AddSnippet.as_view(), name='add'),
#     url(r'^publish/(?P<pk>\d*)/?$', views.PublishSnippet.as_view(), name='publish'),
#     
#     # Dashboard
#     url(r'^$', views.dashboard, name='dashboard'),
#     url(r'^snippet/author/(?P<pk>\d+)/?$', views.recent_snippets_by_author, name='recent-snippets-by-author'),
#     url(r'^snippet/?$', views.snippet_list, name='snippet-list'),


    url(r'^poetry/tagged/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'type': 'poetry'}, name='tagged-poetry'),
    url(r'^snippet/tagged/(?P<slug>[\w.@+-]+)/?$', views.readers.tagged_items, {'type': 'snippet'}, name='tagged-snippet'),

    url(r'^search/person/?$', views.search.person, name='search-person'),
    url(r'^search/org/?$', views.search.organization, name='search-organization'),
    
    url(r'^$', views.readers.home, name='home'),
    
]