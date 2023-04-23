from django.urls import re_path

from . import views

app_name = 'proofreader'
urlpatterns = [
    
    re_path(r'^$', views.home, name='home'),
    re_path(r'^poetry/(?P<pk>\d+)?$', views.proofread_poetry, name='poetry'),
    
]
