from django.conf.urls import patterns, include, url
from measureTools import views

urlpatterns = patterns('',
    url(r'^$', views.selectToolView.as_view() , name = 'select_tool'),
)
