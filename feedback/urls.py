from django.conf.urls import include, url, patterns

from . import views


urlpatterns = [

    #url(r'^(?P<app>[-\w]+)/(?P<model>[-\w]+)/(?P<obj_id>\d+)/?$', views.FeedbackCreateView.as_view(), name='add_for_content'),
    url(r'^list/?$', views.feedback_list, name='feedback-list'),
    url(r'^(?P<ctype_id>\d+)/(?P<obj_id>\d+)/?$', views.FeedbackCreateView.as_view(), name='add_for_content'),    
    url(r'^$', views.FeedbackCreateView.as_view(), name='add'),
]