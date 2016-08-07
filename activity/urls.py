from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.activity_list, name='activity-list'),

]