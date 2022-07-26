from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Film

from random import choice
from datetime import date

def list_films(request):
	will_watch_film_list = Film.objects.order_by('title').filter(watched=False)
	watched_film_list = Film.objects.order_by('title').filter(watched=True)
	context = {
		'will_watch_film_list': will_watch_film_list,
		'watched_film_list': watched_film_list,
	}
	return render(request, 'films/list_films.html', context)


def detail_film(request, film_id):
	film = get_object_or_404(Film, pk=film_id)
	return render(request, 'films/detail_film.html', {'film': film})


def my_films(request, film_id=0):
	if film_id > 0:
		return detail_film(request, film_id)
	else:
		return list_films(request)


def random_film(request):
	film_list = Film.objects.filter(watched=False)
	film_id = choice(film_list).id
	return detail_film(request, film_id)


def new_film(request):
	current_year = str(date.today().year)
	return render(request, 'films/new_film.html', {'current_year': current_year})


def create_film(request):
	film = Film.objects.create(title=request.POST['title'], year=request.POST['year'], description=request.POST['description'])
	return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))


def edit_film(request):
	film = get_object_or_404(Film, pk=request.POST['id'])
	film.title = request.POST['title']
	film.year = request.POST['year']
	film.description = request.POST['description']
	film.watched = request.POST['watched']
	film.save()
	return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))


def delete_film(request):
	film = get_object_or_404(Film, pk=request.POST['id'])
	film.delete()
	return HttpResponseRedirect(reverse('films:list'))



"""
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def request_db(request):
	if request.method == 'GET':
		return HttpResponse('GET succed')
	
	elif request.method == 'POST':
		film = Film.objects.create(title=request.POST['title'], year=request.POST['year'], description=request.POST['description'])
		return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))
	
	elif request.method == 'PUT':
		return HttpResponse(request)
		#film = get_object_or_404(Film, pk=film_id)
		#return HttpResponseRedirect(reverse('films:detail', args=(film.id,)))
	
	elif request.method == 'DELETE':
		return HttpResponse('DELETE succed')
	
	else:
		return HttpResponse(f"Method '{request.method}' ins't compatible.")
"""

# def create_film(request):
# 	title = f"""<pre>
# <h1>scheme</h1> {request.scheme}
# <h1>body</h1> {request.body}
# <h1>path</h1> {request.path}
# <h1>path_info</h1> {request.path_info}
# <h1>method</h1> {request.method}
# <h1>encoding</h1> {request.encoding}
# <h1>content_type</h1> {request.content_type}
# <h1>content_params</h1> {request.content_params}
# <h1>GET</h1> {dict(request.GET)}
# <h1>POST</h1> {dict(request.POST)}
# <h1>COOKIES</h1> {request.COOKIES}
# <h1>FILES</h1> {dict(request.FILES)}
# <h1>META</h1> {request.META}
# <h1>headers</h1> {request.headers}
# <h1>resolver_match</h1> {request.resolver_match}
# </pre>"""
#
# 	#title = str(title)
# 	return HttpResponse(title)