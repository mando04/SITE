from django.shortcuts import render_to_response, RequestContext

def home(request):
	TITLE = 'Profile'
	return render_to_response('users/home.html', { 'TITLE' : TITLE}, context_instance=RequestContext(request))