from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
	return render(request, 'frontend/index.html',
		{'form_creation': UserCreationForm})