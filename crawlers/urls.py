from django.conf.urls import url

from . import views

app_name = 'crawlers'
urlpatterns = [
    
    url(r'^article/add-poetry$', views.article_to_poetry, name='article-to-poetry'),
    
    url(r'^article/(?P<pk>\d+)$', views.raw_article_details, name='article-details'),
    url(r'^article/?$', views.raw_article_list, name='article-list'),
    
    url(r'^author/(?P<pk>\d+)$', views.raw_author_details, name='author-details'),    
    url(r'^author/?$', views.raw_author_list, name='author-list'),
    
    url(r'^ajax/readable/?$', views.fetch_readable, name='readable'),
    
    url(r'^$', views.home, name='home'),
]