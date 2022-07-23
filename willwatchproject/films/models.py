from django.db import models


class Film(models.Model):
	title = models.CharField(max_length=100, unique=True) # obl unique
	year = models.IntegerField(null=True, blank=True) # non-obl
	description = models.CharField(max_length=500, null=True, blank=True) # non-obl
	watched = models.BooleanField(default=False) # obl
	"""
	# Choose one: Image or URL
	image = models.ImageField(upload_to=None, max_length=100, height_field=None, width_field=None, null=True, blank=True) # non-obl
	image = models.URLField(max_length=200, null=True, blank=True) #non-obl
	"""

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


