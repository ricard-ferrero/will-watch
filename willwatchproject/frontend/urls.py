from django.urls import path
from . import views
#from django.views.generic import TemplateView

app_name = 'frontend'
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('signout/', views.signout, name='signout'),
]