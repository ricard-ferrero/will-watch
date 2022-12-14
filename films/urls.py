from django.urls import path
from . import views

app_name = 'films'
urlpatterns = [
	path('myfilms/', views.my_films, name='list'),
	path('myfilms/<int:film_id>/', views.my_films, name='detail'),
	path('random/', views.random_film, name='random'),
	path('new/', views.new_film, name='new'),
	path('edit/<int:pk>/', views.update_film, name='update'),
	path('remove/<int:pk>/', views.delete_film, name='delete'),
	path('changewhatched/<int:pk>/', views.whatched_film, name='watched'),
]