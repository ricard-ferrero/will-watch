from django.db import models
from films.models import Film
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
	genre_name = models.CharField(max_length=50) # obl
	films = models.ManyToManyField(Film)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.genre_name

	def get_absolute_url(self):
		return reverse('genres:list')