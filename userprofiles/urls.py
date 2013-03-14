from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'userprofiles.views.home', name='user-home')
)