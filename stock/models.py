from __future__ import unicode_literals

from django.db import models
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


#@python_2_unicode_compatible
class Stock(models.Model):
	username=models.ForeignKey(User)
	quote=models.CharField(max_length=50)
	qty=models.IntegerField(default=0)
	#price=models.DecimalField(max_digits=20,decimal_places=5)
	def __str__(self):
		return "%s %s %s" %(self.username,self.quote,self.qty)
	
#User.stock=property(lambda u: Stock.objects.get_or_create(username=u)[:])

class Location(models.Model):
	username=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
	city=models.CharField(max_length=20)
	state=models.CharField(max_length=20)
	#zipcode=models.CharField(max_length=10)
	def __unicode__(self):
		return '%s %s %s' %(self.username,self.city,self.state)
	
User.location=property(lambda u: Location.objects.get_or_create(username=u)[0])
