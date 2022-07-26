from django.urls import path
from . import views

app_name = 'films'
urlpatterns = [
	# GET
	path('myfilms/', views.my_films, name='list'),
	path('myfilms/<int:film_id>/', views.my_films, name='detail'),
	path('random/', views.random_film, name='random'),
	# POST
	path('new/', views.new_film, name='new'),
	path('create/', views.create_film, name='create'),
	# PUT
	path('edit/', views.edit_film, name='edit'),
	# DELETE
	path('delete/', views.delete_film, name='delete'),

	# # REQUEST DB
	# path('request_db/', views.request_db, name='request_db'),
]