from django.conf.urls import re_path

from . import views

urlpatterns = [

    # Dashboard
    re_path(r'^search/?$', views.site_search, name='site-search'),
    re_path(r'^advancesearch/?$', views.site_advance_search, name='site-advance-search'),
       
]
