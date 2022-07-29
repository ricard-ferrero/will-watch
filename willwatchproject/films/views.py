from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Film
from genres.models import Genre

from random import choice
from datetime import date


def my_films(request, film_id=0):
	if film_id > 0:
		return detail_film(request, film_id)
	else:
		return list_films(request)


def list_films(request):
	will_watch_film_list = Film.objects.order_by('title').filter(watched=False)
	watched_film_list = Film.objects.order_by('title').filter(watched=True)
	genres_list = Genre.objects.order_by('genre_name')
	context = {
		'will_watch_film_list': will_watch_film_list,
		'watched_film_list': watched_film_list,
		'genres_list': genres_list
	}
	return render(request, 'films/list_films.html', context)


def detail_film(request, film_id):
	if request.method == 'GET':
		film = get_object_or_404(Film, pk=film_id)
		return render(request, 'films/detail_film.html', {'film': film})
	elif request.method == 'POST':
		if request.POST['call-to'] == 'delete':
			return delete_film(request)
		elif request.POST['call-to'] == 'edit':
			return edit_film(request)
		else:
			return HttpResponseRedirect(reverse('films:list'))


def random_film(request):
	film_list = Film.objects.filter(watched=False)
	film_id = choice(film_list).id
	return detail_film(request, film_id)


def new_film(request):
	if request.method == 'GET':
		genres_list = Genre.objects.order_by('genre_name')
		return render(request, 'films/new_film.html', {'genres_list': genres_list})
	elif request.method == 'POST':
		return create_film(request)


def create_film(request):
	film = Film(title=request.POST['title'])
	if request.POST['year']:
		film(year=request.POST['year'])
	if request.POST['description']:
		film(description=request.POST['description'])
	film.save()
	genres_list = request.POST.getlist('genre')
	for i in genres_list:
		film.genre_set.add(i)
	print(film.genre_set.all())
	return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))


def edit_film(request):
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
	film.save()
	return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))
	

def delete_film(request):
	film = get_object_or_404(Film, pk=request.POST['id'])
	film.delete()
	return HttpResponseRedirect(reverse('films:list'))