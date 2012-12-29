from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'www.views.home'),
	url(r'^post/modify/(?P<post>\w)/$', 'www.views.postModify'),
    url(r'^admin/', include(admin.site.urls)),
)
