from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.snippet_details, name='view'),
    url(r'^add/(?P<pk>\d*)/?$', views.AddSnippet.as_view(), name='add'),
    
    # Dashboard
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^snippet/?$', views.snippet_list, name='snippet-list'),
    url(r'^tag/?$', views.tag_list, name='tag-list'),
    
]