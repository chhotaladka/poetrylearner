from django.conf.urls import url

from . import views

urlpatterns = [

    # Dashboard
    url(r'^search/?$', views.site_search, name='site-search'),
    url(r'^advancesearch/?$', views.site_advance_search, name='site-advance-search'),
    url(r'^$', views.welcome, name='welcome'),
       
]