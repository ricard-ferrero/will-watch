#from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'films': self.object.films.all().order_by('title').filter(watched=False),
			'films_watched': self.object.films.all().order_by('title').filter(watched=True),
			})
		return context


class GenreUpdateView(UpdateView):
	model = Genre
	fields = ['genre_name']
	template_name = 'genres/update_genre.html'
	success_url = reverse_lazy('genres:list')


class GenreDeleteView(DeleteView):
	model = Genre
	template_name = 'genres/delete_genre.html'
	success_url = reverse_lazy('genres:list')