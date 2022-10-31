from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
	title = models.CharField(max_length=100) # obl unique
	year = models.IntegerField(null=True, blank=True) # non-obl
	description = models.CharField(max_length=500, null=True, blank=True) # non-obl
	watched = models.BooleanField(default=False) # obl
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


