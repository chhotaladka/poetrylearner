from django.conf.urls import url

from . import views

app_name = 'proofreader'
urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    url(r'^poetry/(?P<pk>\d+)?$', views.proofread_poetry, name='poetry'),
    
]