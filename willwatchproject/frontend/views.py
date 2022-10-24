from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from django.db import IntegrityError

# Create your views here.
def index(request):
	return render(request, 'frontend/index.html')

def signup(request):
	# not POST
	if request.method == 'GET':
		return render(request, 'frontend/signup.html')

	# POST from signup form
	if request.POST['password1'] == request.POST['password2']:
		try:
			user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
			user.save()
			login(request, user)
			return render(request, 'frontend/index.html')
		except IntegrityError:
			return render(request, 'frontend/signup.html', {'message':'User allready exists', 'type_message':'danger'})
		else:
			return render(request, 'frontend/signup.html', {'message':'Some error happened.\nSorry, try again', 'type_message':'warning'})

	return render(request, 'frontend/signup.html', {'message':'Passwords do not match', 'type_message':'danger'})

def signout(request):
	logout(request)
	return redirect('frontend:index')