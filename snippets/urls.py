from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^(?P<pk>\d+)/?$', views.snippet_details, name='view'),
    url(r'^add/(?P<pk>\d*)/?$', views.AddSnippet.as_view(), name='add'),
    url(r'^publish/(?P<pk>\d*)/?$', views.PublishSnippet.as_view(), name='publish'),
    
    # Dashboard
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^snippet/author/(?P<pk>\d+)/?$', views.recent_snippets_by_author, name='recent-snippets-by-author'),
    url(r'^snippet/?$', views.snippet_list, name='snippet-list'),
    url(r'^tagged/(?P<slug>[\w.@+-]+)/?$', views.tagged_list, name='tagged-list'),
    url(r'^tag/?$', views.tag_list, name='tag-list'),
    
]