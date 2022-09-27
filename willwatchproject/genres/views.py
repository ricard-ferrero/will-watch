#from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Genre

class GenreCreateView(CreateView):
	model = Genre
	fields = ['genre_name']
	template_name = 'genres/new_genre.html'