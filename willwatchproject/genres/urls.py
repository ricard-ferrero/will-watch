from django.urls import path
from . import views

app_name = 'genres'
urlpatterns = [
	path('new/', views.GenreCreateView.as_view(), name='new'),
]