from django.db import models
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
	title = models.CharField(max_length=32)
	content = models.TextField()
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now=True, auto_now_add=True)
	
	def __unicode__(self):
		return self.title