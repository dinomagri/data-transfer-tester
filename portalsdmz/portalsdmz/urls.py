from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'portalsdmz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('userManagement.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^measureTools/', include('measureTools.urls')),
    url(r'^scenarios/', include('scenarios.urls')),
)
