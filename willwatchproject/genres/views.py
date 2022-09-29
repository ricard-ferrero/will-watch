#from django.shortcuts import render
from django.urls import reverse

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Genre


class GenreCreateView(CreateView):
	model = Genre
	fields = ['genre_name']
	template_name = 'genres/new_genre.html'


class GenreListView(ListView):
	model = Genre
	template_name = 'genres/list_genres.html'
	context_object_name = 'genres'

	def get_queryset(self):
		return Genre.objects.order_by('genre_name')


class GenreDetailView(DetailView):
	model = Genre
	template_name = 'genres/detail_genre.html'
	