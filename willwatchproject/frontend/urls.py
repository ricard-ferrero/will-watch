from django.urls import path
from . import views


app_name = 'frontend'
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('signout/', views.signout, name='signout'),
	path('signin/', views.signin, name='signin'),
	path('edituser/', views.edit_user, name='edit_user'),
	path('edituser/<str:msg>', views.edit_user, name='edit_user_msg'),
	path('username/', views.change_username, name='change_username'),
	path('password/', views.change_password, name='change_password'),
]