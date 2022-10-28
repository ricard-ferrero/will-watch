from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.db import IntegrityError

from genres.models import Genre


def index(request):
	return render(request, 'frontend/index.html')


# NEW user
def signup(request):
	# not POST
	if request.method != 'POST':
		return render(request, 'frontend/signup.html')

	# POST from signup form
	if request.POST['password1'] == request.POST['password2']:
		try:
			user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
			user.save()

			genres = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'science fiction', 'thriller', 'western']
			for g in genres:
				new_genre = Genre(genre_name=g, user_id=user.id)
				new_genre.save()
			login(request, user)
			return render(request, 'frontend/index.html')
		except IntegrityError:
			return render(request, 'frontend/signup.html', {'message':'User allready exists', 'type_message':'danger'})
		else:
			return render(request, 'frontend/signup.html', {'message':'Some error happened.\nSorry, try again', 'type_message':'warning'})

	return render(request, 'frontend/signup.html', {'message':'Passwords do not match', 'type_message':'danger'})


# CLOSE session
def signout(request):
	logout(request)
	return redirect('frontend:index')


# OPEN session
def signin(request):
	if request.method != 'POST':
		return redirect('frontend:index')

	user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

	if user is None:
		return render(request, 'frontend/index.html', {'message': 'Username or password is incorrect', 'type_message':'danger'})
	
	login(request, user)
	return redirect('frontend:index')

	