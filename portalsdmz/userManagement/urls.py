from django.conf.urls import patterns, include, url
from userManagement import views

urlpatterns = patterns('',
    url(r'^$', 'userManagement.views.user_login' , name='login'),
    url(r'^logout/$', 'userManagement.views.user_logout', name='logout'),
)
