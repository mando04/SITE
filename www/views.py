from django.shortcuts import render_to_response, RequestContext
from www.models import Post
from django.contrib.auth.models import User
from www.forms import modifyPost, loginForms, regforms
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

def logActivity(request):
	print "User %s hit '%s'"%(request.user, request.META['PATH_INFO'])
	
def home(request):
	TITLE = "Welcome Home!"
	blog_p = Post.objects.all()
	logActivity(request)
	content = {
	'TITLE': TITLE,
	'Post': blog_p,
	}
	return render_to_response('home.html', content, context_instance=RequestContext(request))

def logoutUser(request):
	logout(request)
	return HttpResponseRedirect('/')

def loginUser(request):
	TITLE = 'Please Login!'
	
	""" Catch the Refering url to send user to where they coming from after login """
	print request.META['QUERY_STRING'].split('&')[0].split('=')[-1]
	if request.META['QUERY_STRING'] != "":
		URL_LOGIN = '/login/?next=' + request.META['QUERY_STRING'].split('&')[0].split('=')[-1]
		print 'Got location coming from %s'%URL_LOGIN
	else:
		URL_LOGIN = '/login/'
	print URL_LOGIN
	
	# Catch user if already logged in and redirect them to refere or /
	if request.user.is_authenticated():
		if 'next' in request.META['QUERY_STRING']:
			# split Query string by '&' and 'next' should always be first
			# split the first(item[0]) item in the list and split it by '=' 
			# and grab the last item in the list
			return HttpResponseRedirect(request.META['QUERY_STRING'].split('&')[0].split('=')[-1])
		else:
			return HttpResponseRedirect('/')
			## continue loggin logic
	if request.method == 'POST':
		f = loginForms(request.POST)
		if f.is_valid():
			user = authenticate(username=f.cleaned_data['username'].lower(),
								password=f.cleaned_data['password1'] )
			if user is not None:
				if user.is_active:
					login(request, user)
					ref = request.META['QUERY_STRING'].split('&')[0].split('=')[-1]
					return HttpResponseRedirect(ref)
				else:
					""" account is locked out"""
					#raise Exception, 'Invalid login attempt for %s'%user['username']
					print user.email + 'is locked out!'
					msg = 1
					return render_to_response('login.html', { 'TITLE' : TITLE, 'forms' : f, 'ERROR' : msg, 'URL_LOGIN' : URL_LOGIN  },
												context_instance=RequestContext(request))
			else:
				""" Invalid Username """
				msg = 1
				return render_to_response('login.html', { 'TITLE' : TITLE, 'forms' : f, 'ERROR' : msg, 'URL_LOGIN' : URL_LOGIN },
											context_instance=RequestContext(request))
		else:
			""" Forms is not valid """
			msg = 1
			return render_to_response('login.html', { 'TITLE' : TITLE, 'forms' : f, 'ERROR' : msg, 'URL_LOGIN' : URL_LOGIN }, 
										context_instance=RequestContext(request))
	forms = loginForms()
	return render_to_response('login.html', { 'TITLE' : TITLE, 'forms' : forms, 'URL_LOGIN' : URL_LOGIN, 'request' : request }, context_instance=RequestContext(request))
	
@login_required
def postModify(request, post):
	try:
		post = Post.objects.get(id=post)
	except Exception as e:
		error = e
		return render_to_response('post/modify.html', { 'TITLE' : 'NONE', 'ERROR' : error}, context_instance=RequestContext(request))
	# this will allow admin users to be able to modify all posts
	if request.user.is_superuser:
		pass
	elif request.user.is_staff == False and request.user.username != post.author:
		return render_to_response('post/modify.html', { 'TITLE' : 'NONE', 'ERROR' : 'You are not an admin so you cannot modify other peoples post!' }, context_instance=RequestContext(request))

	TITLE = 'Modify post: %s'%str(post.title)
	# get post data from post and assign it to a hash table to later add to forms values
	data = {
				'title' : post.title,
				'content' : post.content
			}
	# Assign data to forms
	forms = modifyPost(data)
	
	if request.method == 'POST':
		forms = modifyPost(request.POST)
		if forms.is_valid():
			p = post
			p.title = forms.cleaned_data['title']
			p.content = forms.cleaned_data['content']
			p.save()
			return HttpResponseRedirect('/')
	return render_to_response('post/modify.html', { 'TITLE' : TITLE, 'forms' : forms, 'post' : post },
	 							context_instance=RequestContext(request))

@login_required
def postDestroy(request, post):
	try:
		post = Post.objects.get(id=post)
		TITLE = post.title
	except Exception as e:
		error = e
		return render_to_response('post/destroy.html', { 'TITLE' : 'NONE', 'ERROR' : error}, context_instance=RequestContext(request))

	# this will allow admin users to be able to modify all posts
	if request.user.is_superuser:
		pass
	elif request.user.is_staff == False and request.user.username != post.author:
		return render_to_response('post/destroy.html', { 'TITLE' : 'NONE', 'ERROR' : 'You are not allowed to destroy posts!'}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		try:
			post.delete()
			return HttpResponseRedirect('/')
		except Exception as e:
			error = e
			return render_to_response('post/destroy.html', { 'post' : post, 'TITLE' : TITLE, 'ERROR' : error}, context_instance=RequestContext(request))
	return render_to_response('post/destroy.html', { 'TITLE' : TITLE, 'post' : post}, context_instance=RequestContext(request))

@login_required
def blogPost(request):
	TITLE = 'Add a Blog post!'
	# check and see if user is allowed to post
	if request.user.is_staff:
		pass
	else:
		return render_to_response('post/post.html', { 'TITLE' : TITLE, 'ERROR' : 'You are not allowed to post!'}, context_instance=RequestContext(request))

	forms = modifyPost()
	if request.method == 'POST':
		forms = modifyPost(request.POST)
		if forms.is_valid():
			try:
				newPost = Post(title=forms.cleaned_data['title'], content=forms.cleaned_data['content'], author=request.user)
				newPost.save()
				return HttpResponseRedirect('/')
			except Exception as e:
				error = e
				return render_to_response('post/post.html', { 'ERROR' : error, 'TITLE' : TITLE, 'forms' : forms}, context_instance=RequestContext(request))	
	return render_to_response('post/post.html', { 'TITLE' : TITLE, 'forms' : forms}, context_instance=RequestContext(request))

def registerUser(request):
	# Make sure the user is not already logged in
	# we dont want user to be able to register new users
	# if they are already logged in.... no reason right?
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	# start registerUser view
	TITLE = 'Register new User!'
	forms = regforms() # preload forms
	
	# if user submits the form perform the following functions
	if request.method == 'POST':
		forms = regforms(request.POST) # load submitted data into reforms and put in forms var
		
		# check and see if the form is valid
		if forms.is_valid(): 
			usrname = forms.cleaned_data['username'].lower()
			email = forms.cleaned_data['email']
			fname = forms.cleaned_data['fname']
			lname = forms.cleaned_data['lname']
			# check and make sure pass1 and pass2 match
			if forms.cleaned_data['pass1'] == forms.cleaned_data['pass2']:
				password1 = forms.cleaned_data['pass1']
			else: 
				return render_to_response('register_user.html', { 'TITLE' : TITLE, 'forms' : forms, 'ERROR': 'Passwords didn\'t match'}, context_instance=RequestContext(request))
			try:
				newuser = User.objects.create_user(usrname, email, password1)
				return HttpResponseredirect('/login/')
			except Exception as e:
				error = 'Username already exists!'
				return render_to_response('register_user.html', { 'TITLE' : TITLE, 'forms' : forms, 'ERROR' : error}, context_instance=RequestContext(request))
		# if form is not valid return errors to user for fixing....
		else:
			error = 'Please fill out the forms correctly!'
			return render_to_response('register_user.html', { 'TITLE' : TITLE, 'forms' : forms, 'ERROR': error}, context_instance=RequestContext(request))
	return render_to_response('register_user.html', { 'TITLE' : TITLE, 'forms' : forms}, context_instance=RequestContext(request))	
