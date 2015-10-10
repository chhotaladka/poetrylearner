from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.snippet_details, name='view'),
    url(r'^add/(?P<pk>\d*)/?$', views.AddSnippet.as_view(), name='add'),
    
]