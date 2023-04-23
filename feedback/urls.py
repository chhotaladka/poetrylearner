from django.urls import re_path

from . import views

app_name = 'feedback'
urlpatterns = [

    re_path(r'^(?P<pk>\d+)$', views.feedback_response, name='response'),
    re_path(r'^$', views.feedback_list, name='list'),
    
    re_path(r'^add/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/?$', views.FeedbackCreateView.as_view(), name='add_for_content'),
    re_path(r'^add/?$', views.FeedbackCreateView.as_view(), name='add'),
]
