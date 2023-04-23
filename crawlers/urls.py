from django.urls import re_path

from . import views

app_name = 'crawlers'
urlpatterns = [
    
    re_path(r'^article/add-poetry$', views.article_to_poetry, name='article-to-poetry'),
    
    re_path(r'^article/(?P<pk>\d+)$', views.raw_article_details, name='article-details'),
    re_path(r'^article/?$', views.raw_article_list, name='article-list'),
    
    re_path(r'^author/(?P<pk>\d+)$', views.raw_author_details, name='author-details'),
    re_path(r'^author/?$', views.raw_author_list, name='author-list'),
    
    re_path(r'^ajax/readable/?$', views.fetch_readable, name='readable'),
    
    re_path(r'^$', views.home, name='home'),
]
