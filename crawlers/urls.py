from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^article/(?P<pk>\d+)$', views.RawArticleDetails, name='article-details'),
    
]