from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^all/?$', views.activity_list_all, name='list-all'),
    url(r'^$', views.activity_list, name='list'),

]