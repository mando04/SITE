from django.db import models
from django.contrib.auth.models import User
import datetime



class Post(models.Model):
	title = models.CharField(max_length=32)
	content = models.TextField()
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)	
	
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ['-date']

class Comments(models.Model):
	author = models.CharField(max_length=32, null=True)
	email = models.EmailField(null=False)
	comment = models.TextField()
	date = models.DateTimeField(auto_now=True, auto_now_add=True)
	post = models.ForeignKey(Post)
	
	def __unicode__(self):
		return self.author
