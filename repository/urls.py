from django.conf.urls import url

from . import views

urlpatterns = [
    
#     url(r'^add/person/(?P<pk>\d*)/?$', views.writers.AddPerson.as_view(), name='add-person'),
#     url(r'^add/organization/(?P<pk>\d*)/?$', views.writers.AddOrg.as_view(), name='add-org'),
#     url(r'^add/place/(?P<pk>\d*)/?$', views.writers.AddPlace.as_view(), name='add-place'),
#     url(r'^add/product/(?P<pk>\d*)/?$', views.writers.AddProduct.as_view(), name='add-product'),
#     url(r'^add/event/(?P<pk>\d*)/?$', views.writers.AddEvent.as_view(), name='add-event'),
#     url(r'^add/book/(?P<pk>\d*)/?$', views.writers.AddBook.as_view(), name='add-book'),
#     url(r'^add/poetry/(?P<pk>\d*)/?$', views.writers.AddPoetry.as_view(), name='add-poetry'),
#     url(r'^add/snippet/(?P<pk>\d*)/?$', views.writers.AddSnippet.as_view(), name='add-snippet'),
    
    url(r'^add/(?P<type>[\w.@+-]+)/(?P<pk>\d+)?/?$', views.writers.AddItem.as_view(), name='add-item'),
    url(r'^add/?$', views.writers.add, name='add'),
    
    url(r'^data/(?P<type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/publish/?$', views.writers.publish, name='publish'),
    
    url(r'^data/(?P<type>[\w.@+-]+)/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.readers.item, name='item'),
    url(r'^data/(?P<type>[\w.@+-]+)/?$', views.readers.list, name='list'),
    url(r'^data/?$', views.readers.items, name='items'),
    
#     url(r'^(?P<pk>\d+)/?$', views.snippet_details, name='view'),
#     url(r'^add/(?P<pk>\d*)/?$', views.AddSnippet.as_view(), name='add'),
#     url(r'^publish/(?P<pk>\d*)/?$', views.PublishSnippet.as_view(), name='publish'),
#     
#     # Dashboard
#     url(r'^$', views.dashboard, name='dashboard'),
#     url(r'^snippet/author/(?P<pk>\d+)/?$', views.recent_snippets_by_author, name='recent-snippets-by-author'),
#     url(r'^snippet/?$', views.snippet_list, name='snippet-list'),
#     url(r'^tagged/(?P<slug>[\w.@+-]+)/?$', views.tagged_list, name='tagged-list'),
#     url(r'^tag/?$', views.tag_list, name='tag-list'),
    
]