from django.urls import re_path

from . import views

app_name = 'activity'
urlpatterns = [

    re_path(r'^all/?$', views.activity_list_all, name='list-all'),
    re_path(r'^contributors/?$', views.list_contributors, name='contributors'),
    
    re_path(r'^ajax/contributors/?$', views.ajax_contributors, name='ajax-contributors'),
    
    re_path(r'^$', views.activity_list, name='list'),

]
