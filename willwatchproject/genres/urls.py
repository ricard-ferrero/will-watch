from django.urls import path
from . import views

app_name = 'genres'
urlpatterns = [
	path('new/', views.GenreCreateView.as_view(), name='new'),
	path('list/', views.GenreListView.as_view(), name='list'),
	path('detail/<int:pk>/', views.GenreDetailView.as_view() , name='detail'),
]