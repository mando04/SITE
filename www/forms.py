from django import forms
from django.contrib.auth.models import User
from www.models import Post

class modifyPost(forms.Form):
    title = forms.CharField(max_length=32)
    content = forms.CharField(widget=forms.Textarea(attrs={ 'cols' : 50, 'rows' : 5 }))
