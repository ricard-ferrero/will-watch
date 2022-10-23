from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login #cookie login

from django.db import IntegrityError

# Create your views here.
def index(request):
	return render(request, 'frontend/index.html')

def signup(request):
	# not POST
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('frontend:index'))

	# POST from signup form
	if request.POST['password1'] == request.POST['password2']:
		try:
			user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
			user.save()
			login(request, user)
			return render(request, 'frontend/index.html', {'message':'OK', 'type_message':'success'})
		except IntegrityError:
			return render(request, 'frontend/index.html', {'message':'User allready exists', 'type_message':'danger'})
		else:
			return render(request, 'frontend/index.html', {'message':'Some error happened.\nSorry, try again', 'type_message':'warning'})

	return render(request, 'frontend/index.html', {'message':'Passwords do not match', 'type_message':'danger'})