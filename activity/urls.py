from django.conf.urls import url

from . import views

app_name = 'activity'
urlpatterns = [

    url(r'^all/?$', views.activity_list_all, name='list-all'),
    url(r'^contributors/?$', views.list_contributors, name='contributors'),
    
    url(r'^ajax/contributors/?$', views.ajax_contributors, name='ajax-contributors'),
    
    url(r'^$', views.activity_list, name='list'),

]