from django.db import models
from films.models import Film
from django.urls import reverse


class Genre(models.Model):
	genre_name = models.CharField(max_length=50, unique=True) # obl
	#logo = models.ImageField(upload_to=None, max_length=100, height_field=None, width_field=None, null=True, blank=True) # non-obl
	films = models.ManyToManyField(Film)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.genre_name

	def get_absolute_url(self):
		return reverse('films:list')