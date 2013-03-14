from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'www.views.home', name='home'),
	url(r'^login/$', 'www.views.loginUser', name='login'),
	url(r'^logout/$', 'www.views.logoutUser', name='logout'),
	url(r'^post/$', 'www.views.blogPost', name='NewPost'),
	url(r'^register/', 'www.views.registerUser', name='RegisterNewUser'),
	url(r'^post/modify/(?P<post>\w)/$', 'www.views.postModify'),
	url(r'^post/destroy/(?P<post>\w)/$', 'www.views.postDestroy'),
    url(r'^admin/', include(admin.site.urls)),
	(r'^users/', include('userprofiles.urls')),
)
