from django.conf.urls import include, url, patterns

from . import views


urlpatterns = [

    url(r'^data/(?P<pk>\d+)$', views.feedback_response, name='response'),
    url(r'^data/?$', views.feedback_list, name='list'),
    
    url(r'^add/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/?$', views.FeedbackCreateView.as_view(), name='add_for_content'),    
    url(r'^add/?$', views.FeedbackCreateView.as_view(), name='add'),
]