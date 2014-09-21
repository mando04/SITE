from django import forms
from django.contrib.auth.models import User

class modifyPost(forms.Form):
    title = forms.CharField(max_length=32)
    content = forms.CharField(widget=forms.Textarea(attrs={ 'cols' : 50, 'rows' : 5 }))

class loginForms(forms.Form):
	username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(attrs={ 'placeholder' : 'Username'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False, attrs={'placeholder' : 'Pasword'}))

class regforms(forms.Form):
	username = forms.CharField(label='Username', max_length=32)
	fname = forms.CharField(label='First Name', max_length=32)
	lname = forms.CharField(label='Last Name', max_length=32)
	email = forms.EmailField(label='Valid E-mail')
	bday = forms.DateField(label='Birthday', required=True)
	wsite = forms.URLField(label='Website', required=False)
	pass1 = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(render_value=False))
	pass2 = forms.CharField(label='Re-type Password:', max_length=32, widget=forms.PasswordInput(render_value=False))
	