from django.conf.urls import url

from . import views

app_name = 'feedback'
urlpatterns = [

    url(r'^(?P<pk>\d+)$', views.feedback_response, name='response'),
    url(r'^$', views.feedback_list, name='list'),
    
    url(r'^add/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/?$', views.FeedbackCreateView.as_view(), name='add_for_content'),    
    url(r'^add/?$', views.FeedbackCreateView.as_view(), name='add'),
]