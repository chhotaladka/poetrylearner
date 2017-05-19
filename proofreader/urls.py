from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    url(r'^poetry/(?P<pk>\d+)?$', views.proofread_poetry, name='poetry'),
    
]