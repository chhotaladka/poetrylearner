from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^article/(?P<pk>\d+)$', views.raw_article_details, name='article-details'),
    url(r'^article/?$', views.raw_article_list, name='article-list'),
    
]