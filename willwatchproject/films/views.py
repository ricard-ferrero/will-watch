from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import DetailView
from django.views.generic.list import ListView

from .models import Film
from genres.models import Genre

from random import choice
from datetime import date


@login_required
def my_films(request, film_id=0):
	if film_id > 0:
		if request.method == 'POST':
			return post_detail_film(request, film_id)
		return FilmDetailView.as_view()(request, pk=film_id)
	else:
		return FilmsListView.as_view()(request)


class FilmsListView(ListView):
	template_name = 'films/list_films.html'
	context_object_name = 'will_watch_film_list'
	model = Film

	def get_queryset(self):
		return Film.objects.order_by('title').filter(watched=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'watched_film_list': Film.objects.order_by('title').filter(watched=True),
			'genres_list': Genre.objects.order_by('genre_name')
			})
		return context


class FilmDetailView(DetailView):
	model = Film
	template_name = 'films/detail_film.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'genres': self.object.genre_set.all(),
			'genres_list': Genre.objects.order_by('genre_name'),
			})
		return context


"""
The rest of the code will be updated to Class Based Views,
then I need to research more about that.
For this moment I prefere to keep it functional and
work on the rest of the project :)
"""

"""
def post_detail_film(request, film_id):
	if request.POST['call-to'] == 'delete':
		return delete_film(request)
	elif request.POST['call-to'] == 'edit':
		return edit_film(request)
	else:
		return HttpResponseRedirect(reverse('films:list'))
"""


@login_required
def random_film(request):
	film_list = Film.objects.filter(watched=False)
	if film_list:
		film_id = choice(film_list).id
		return FilmDetailView.as_view()(request, pk=film_id)
	else:
		return HttpResponseRedirect(reverse('films:list'))


@login_required
def new_film(request):
	if request.method == 'GET':
		genres_list = Genre.objects.order_by('genre_name')
		return render(request, 'films/new_film.html', {'genres_list': genres_list})
	elif request.method == 'POST':
		return create_film(request)


def create_film(request):
	film = Film(title=request.POST['title'])
	if request.POST['year']:
		film.year = request.POST['year']
	if request.POST['description']:
		film.description = request.POST['description']
	film.save()
	genres_list = request.POST.getlist('genre')
	for i in genres_list:
		film.genre_set.add(i)
	return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))


def edit_film(request):
	"""
	The 'request' is a POST with all the information of the film object:
	not only the data to be changed, the data preserved as well.
	"""
	film = get_object_or_404(Film, pk=request.POST['id'])
	film.title = request.POST['title']
	if request.POST['year'] != '' and request.POST['year'] != None:
		film.year = request.POST['year']
	else:
		film.year = None
	if request.POST['description'] != '' and request.POST['description'] != None:
		film.description = request.POST['description']
	else:
		film.description = None
	film.watched = request.POST['watched']
	genres_list = request.POST.getlist('genre')
	film.genre_set.clear()
	for i in genres_list:
		film.genre_set.add(i)
	film.save()
	return HttpResponseRedirect(reverse('films:detail', args=[film.id]))
	

@login_required
def delete_film(request, pk):
	film = get_object_or_404(Film, pk=pk)
	if request.method == 'GET':
		return render(request, 'films/delete_film.html', {'film': film})
	if request.method == 'POST':
		film.delete()
		return HttpResponseRedirect(reverse('films:list'))


@login_required
def update_film(request, pk):
	if request.method == 'GET':
		film = get_object_or_404(Film, pk=pk)
		genres_list = Genre.objects.order_by('genre_name')
		genres_film = film.genre_set.all()
		return render(request, 'films/update_film.html', {'film': film, 'genres_list': genres_list})
	if request.method == 'POST':
		return edit_film(request)


@login_required
def whatched_film(request, pk):
	film = get_object_or_404(Film, pk=pk)
	film.watched = not film.watched
	film.save()
	return HttpResponseRedirect(reverse('films:list'))