from django.db import models
from django.contrib.auth.models import User


class mainProfile(models.Model):
	MOOD = (
				('HAPPY', 'Happy'),
				('SAD', 'Sad'),
				('UPSET', 'Upset'),
				('ANGRY', 'Angry')
			)
	person = models.ForeignKey(User)
	wsite = models.URLField(null=True)
	facebook = models.URLField(null=True)
	linkedin= models.URLField(null=True)
	status = models.CharField(max_length=7, choices=(('ON', 'Online'),('OFF', 'Offline')))
	mood = models.CharField(max_length=5, choices=MOOD)
	
	def __unicode__(self):
		return self.person.username