from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^article/(?P<pk>\d+)$', views.raw_article_details, name='article-details'),
    url(r'^article/?$', views.raw_article_list, name='article-list'),
    
    url(r'^author/(?P<pk>\d+)$', views.raw_author_details, name='author-details'),
    url(r'^author/?$', views.raw_author_list, name='author-list'),
    
    url(r'^$', views.dashboard, name='dashboard'),
]