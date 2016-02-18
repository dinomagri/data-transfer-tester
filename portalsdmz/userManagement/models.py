from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	institution = models.CharField(max_length=120)
 	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

 	def __unicode__(self):
 		return self.user.email