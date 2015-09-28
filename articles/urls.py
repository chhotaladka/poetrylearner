from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.random_article, name='random'),
    url(r'^explore/$', views.explore, name='explore'),
    
    url(r'^article/(?P<pk>\d+)/(?P<slug>[\w.@+-]+)?/?$', views.article_details, name='article-details'),
    url(r'^add/article/(?P<pk>\d*)/?$', views.AddArticle.as_view(), name='add-article'),
    url(r'^edit/article/(?P<pk>\d*)/?$', views.EditArticle.as_view(), name='edit-article'),
]