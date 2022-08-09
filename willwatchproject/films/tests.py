from django.test import TestCase
from django.urls import reverse

from .models import Film
from genres.models import Genre


class FilmModelTests(TestCase):
	def test_film_creation_only_title(self):
		"""
		create a Film object but only setting the title
		and the others fields wild be generetad as "None"
		except "watched" as "False"
		"""

		title = "film title"
		film = Film(title=title)
		self.assertEqual(film.title, title)
		self.assertEqual(film.year, None)
		self.assertEqual(film.description, None)
		self.assertIs(film.watched, False)

	def test_film_creation_all_fields(self):
		"""
		create a Film object with all the fields correctly
		and the field "watched" is "False"
		"""

		title = "film title"
		year = 1999
		description = "Lorem Ipsum és un text de farciment usat per la indústria de la tipografia i la impremta. Lorem Ipsum ha estat el text estàndard de la indústria des de l'any 1500, quan un impressor desconegut va fer servir una galerada de text i la va mesclar per crear un llibre de mostres tipogràfiques. No només ha sobreviscut cinc segles, sinó que ha fet el salt cap a la creació de tipus de lletra electrònics, romanent essencialment sense canvis. Es va popularitzar l'any 1960 amb el llançament de fulls Letraset que contenien passatges de Lorem Ipsum, i més recentment amb programari d'autoedició com Aldus Pagemaker que inclou versions de Lorem Ipsum."
		film = Film(title=title, year=year, description=description)
		self.assertEqual(film.title, title)
		self.assertEqual(film.year, year)
		self.assertEqual(film.description, description)
		self.assertIs(film.watched, False)


class MyFilmsViewTests(TestCase):

	def test_redirecting_to_list_films_without_film_id(self):
		"""
		The URL doesn't contains a film id and the page
		is redirected to the list of films.
		
		The list of films contains a "will watch",
		a "watched" and a "genres" lists
		"""
		response = self.client.get(reverse('films:list'))
		self.assertContains(response, 'Genres')
		self.assertContains(response, 'Will Watch')
		self.assertContains(response, 'Watched')

	def test_redirecting_to_detail_film_with_film_id(self):
		"""
		The URL contains a film id and the page is redirected
		to the detail of the film.
		"""
		film = Film.objects.create(title="title film")
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertContains(response, 'Title')
		self.assertContains(response, film.title)

class ListFilmsViewTests(TestCase):

	def test_film_list_is_empty(self):
		"""
		Doesn't list anything becouse the DB is empty
		"""
		response = self.client.get(reverse('films:list'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['will_watch_film_list'], [])
		self.assertQuerysetEqual(response.context['watched_film_list'], [])

	def test_list_a_film_not_watched(self):
		"""
		Create a Film object and list it in "Will Watch"
		"""
		film = Film.objects.create(title='film')
		response = self.client.get(reverse('films:list'))
		self.assertQuerysetEqual(response.context['will_watch_film_list'], [film])
		self.assertQuerysetEqual(response.context['watched_film_list'], [])

	def test_list_a_film_watched(self):
		"""
		Create a Film and change it to watched. Then list it in "Watched"
		"""
		film = Film.objects.create(title='film', watched=True)
		response = self.client.get(reverse('films:list'))
		self.assertQuerysetEqual(response.context['will_watch_film_list'], [])
		self.assertQuerysetEqual(response.context['watched_film_list'], [film])

	def test_list_the_films_in_alphabetic_order(self):
		"""
		Create few films (watched and not watched) and order it
		alphabeticly
		"""
		film_Z = Film.objects.create(title='Z')
		film_B = Film.objects.create(title='B')
		film_A = Film.objects.create(title='A')
		film_C = Film.objects.create(title='C')
		film_Y = Film.objects.create(title='Y')
		film_X = Film.objects.create(title='X')

		# Will Watch list
		response = self.client.get(reverse('films:list'))
		self.assertQuerysetEqual(response.context['will_watch_film_list'],
			[film_A, film_B, film_C, film_X, film_Y, film_Z])

		
		# Watched list
		film_Z.watched = True
		film_Z.save()
		film_B.watched = True
		film_B.save()
		film_A.watched = True
		film_A.save()
		film_C.watched = True
		film_C.save()
		film_Y.watched = True
		film_Y.save()
		film_X.watched = True
		film_X.save()
		response = self.client.get(reverse('films:list'))
		self.assertQuerysetEqual(response.context['watched_film_list'],
			[film_A, film_B, film_C, film_X, film_Y, film_Z])

	def test_genres_list_is_empty(self):
		"""
		Doesn't list a genre beocuse de DB is empty
		"""
		response = self.client.get(reverse('films:list'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['genres_list'], [])

	def test_list_genres_alphabeticly(self):
		"""
		Create three genres and list them in the correct order.
		"""
		genre_B = Genre.objects.create(genre_name='B')
		genre_Z = Genre.objects.create(genre_name='Z')
		genre_A = Genre.objects.create(genre_name='A')
		genre_C = Genre.objects.create(genre_name='C')
		genre_Y = Genre.objects.create(genre_name='Y')
		genre_X = Genre.objects.create(genre_name='X')

		response = self.client.get(reverse('films:list'))
		self.assertQuerysetEqual(response.context['genres_list'],
			[genre_A, genre_B, genre_C, genre_X, genre_Y, genre_Z])


class DetailFilmViewTests(TestCase):
	"""
	GET method
	"""
	def test_detail_a_film_only_with_title(self):
		"""
		Detail a film that only has a title and no more information.
		Doesn't render a year nor a description.
		"""
		film = Film.objects.create(title='film title')
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, film.title)
		self.assertNotContains(response, 'Year')
		self.assertNotContains(response, 'Description')

	def test_detail_a_film_with_title_and_year(self):
		"""
		Detail a film that has a title and a year.
		Doesn't render a description.
		"""
		film = Film.objects.create(title='film title', year=1999)
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, film.title)
		self.assertContains(response, 'Year')
		self.assertContains(response, film.year)
		self.assertNotContains(response, 'Description')

	def test_detail_a_film_with_title_and_description(self):
		"""
		Detail a film that has a title and a description.
		Doesn't render a year.
		"""
		film = Film.objects.create(title='film title', description='a description')
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, film.title)
		self.assertContains(response, 'Description')
		self.assertContains(response, film.description)
		self.assertNotContains(response, 'Year')

	def test_detail_a_film_with_title_year_and_description(self):
		"""
		Detail a film that has a title, a year and a description.
		"""
		film = Film.objects.create(title='film title', year=1999, description='a description')
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertContains(response, film.title)
		self.assertContains(response, film.year)
		self.assertContains(response, film.description)

	def test_detail_a_film_not_watched(self):
		"""
		Generate a new Film object and make Flase for defect. Show on page.
		"""
		film = Film.objects.create(title='film')
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertContains(response, 'Not yet')

	def test_detail_a_film_watched(self):
		"""
		Generate a new Film object and mark it as watched. Show on page.
		"""
		film = Film.objects.create(title='film', watched=True)
		response = self.client.get(reverse('films:detail', args=(film.id,)))
		self.assertContains(response, 'Watched')


	def test_detail_a_film_with_a_genre(self):
		"""
		Create two diferent genres, but create too a film with only one genre.
		It's only rendered the genre of the film when it's detailed.
		"""
		terror_film = Film.objects.create(title='film')
		terror_genre = Genre.objects.create(genre_name='terror')
		comedy_genre = Genre.objects.create(genre_name='comedy')
		terror_film.genre_set.add(terror_genre)

		response = self.client.get(reverse('films:detail', args=(terror_film.id,)))
		self.assertContains(response, terror_film.title)
		self.assertContains(response, terror_genre.genre_name)
		self.assertNotContains(response, comedy_genre.genre_name)

	def test_detail_a_film_with_three_different_genres(self):
		"""
		Create a film with three genres. The genres must be rendered on the web
		"""
		genre1 = Genre.objects.create(genre_name='genre 1')
		genre2 = Genre.objects.create(genre_name='genre 2')
		genre3 = Genre.objects.create(genre_name='genre 3')
		film = Film.objects.create(title='film')
		film.genre_set.add(genre1)
		film.genre_set.add(genre2)
		film.genre_set.add(genre3)

		response = self.client.get(reverse('films:detail', args=(film.id,)))
		#print(response.content)

		"""self.assertContains(response, genre1.genre_name)
		self.assertContains(response, genre2.genre_name)
		self.assertContains(response, genre3.genre_name)"""

	"""
	POST method
	"""
	def define_data(self, film, call_to, **kwargs):
		"""
		Define the POST data from a film in the correct form
		"""
		from django.forms.models import model_to_dict

		data = model_to_dict(film)
		for i in data:
			if data[i] == None:
				data[i] = ''

		for i in kwargs:
			if i in data:
				data[i] = kwargs[i]
			else:
				print('ERROR: argument doesn\'t exist in model object')

		data['call-to'] = call_to

		return data

	def test_modify_the_title_of_a_film(self):
		"""
		Modify the title of a film but the other things stay intact.
		"""
		old_title = 'title 1'
		new_title = 'title 2'
		
			# First create a Film object with the old title
		film = Film.objects.create(title=old_title)
			# Now create all the data to send
		data = self.define_data(film, 'edit', title=new_title)
			# Send the POST petition
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
			# To compare, we need first to update the Film object
		film = Film.objects.get(pk=film.id)
			# Now we can compare
		self.assertEqual(film.title, new_title)

	def test_modify_the_year_of_a_film(self):
		"""
		Modify the year of a film but the other things stay intact.
		"""
		old_year = 1990
		new_year = 2000
		
			# First create a Film object
		film = Film.objects.create(title='film', year=old_year)
			# Now create all the data to send
		data = self.define_data(film, 'edit', year=new_year)
			# Send the POST petition
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
			# To compare, we need first to update the Film object
		film = Film.objects.get(pk=film.id)
			# Now we can compare
		self.assertEqual(film.year, new_year)

	def test_modify_the_description_of_a_film(self):
		"""
		Modify the description of a film but the other things stay intact.
		"""
		old_description = 'Description'
		new_description = 'Extended description'
		
			# First create a Film object
		film = Film.objects.create(title='film', description=old_description)
			# Now create all the data to send
		data = self.define_data(film, 'edit', description=new_description)
			# Send the POST petition
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
			# To compare, we need first to update the Film object
		film = Film.objects.get(pk=film.id)
			# Now we can compare
		self.assertEqual(film.description, new_description)

	def test_modify_the_watched_of_a_film(self):
		"""
		Modify the 'watched' of a film but the other things stay intact.
		"""
			# First create a Film object
		film = Film.objects.create(title='film')
		self.assertEqual(film.watched, False)
			# Now create all the data to send
		data = self.define_data(film, 'edit', watched=True)
			# Send the POST petition
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
			# To compare, we need first to update the Film object
		film = Film.objects.get(pk=film.id)
			# Now we can compare
		self.assertEqual(film.watched, True)

	def test_delete_a_film(self):
		"""
		Delete a film from the DB
		"""
		film = Film.objects.create(title='film title')
		self.assertQuerysetEqual(Film.objects.all(), [film])

		data = self.define_data(film, 'delete')
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
		self.assertQuerysetEqual(Film.objects.all(), [])


class RandomFilmViewTests(TestCase):
	def test_open_a_detail_page(self):
		"""
		When the random page is open it looks for a detail page
		from a film (random).
		"""
		film_A = Film.objects.create(title='A')
		film_B = Film.objects.create(title='B')
		film_C = Film.objects.create(title='C')
		film_X = Film.objects.create(title='X')
		film_Y = Film.objects.create(title='Y')
		film_Z = Film.objects.create(title='Z')

		response = self.client.get(reverse('films:random'))
		self.assertEqual(response.status_code, 200)

		template = 'films/detail_film.html'
		self.assertTemplateUsed(response, template)


class NewFilmViewTests(TestCase):
	"""
	GET
	"""
	def test_render_new_film_tempate(self):
		"""
		When creating a new film the correct template is rendered
		"""
		response = self.client.get(reverse('films:new'))
		template = 'films/new_film.html'
		self.assertTemplateUsed(response, template)

	def test_list_the_genres_when_creating_a_new_film(self):
		"""
		When createing a new film is loaded the list of genres to
		can select one or more of them
		"""
		genre_A = Genre.objects.create(genre_name='A')
		genre_B = Genre.objects.create(genre_name='B')
		genre_C = Genre.objects.create(genre_name='C')
		
		response = self.client.get(reverse('films:new'))
		self.assertQuerysetEqual(response.context['genres_list'], [genre_A, genre_B, genre_C])

	def test_when_createing_a_new_film_list_genres_alphabeticly(self):
		"""
		When createing a new film is loaded the list of genres and
		are ordered by the name
		"""
		genre_B = Genre.objects.create(genre_name='B')
		genre_C = Genre.objects.create(genre_name='C')
		genre_A = Genre.objects.create(genre_name='A')
		
		response = self.client.get(reverse('films:new'))
		self.assertQuerysetEqual(response.context['genres_list'], [genre_A, genre_B, genre_C])

	"""
	POST
	"""
	def define_data(self, **kwargs):
		data = {
			'title': 'Film title',
			'year': '',
			'description': '',
		}

		for i in kwargs:
			data[i] = kwargs[i]

		return data

	def test_create_a_film_witch_only_has_a_title(self):
		"""
		Send a post to create a film but only contains a title.
		The film is correctly created.
		"""
		# 1. Send the POST with the needed data (without a genre list)
		data = self.define_data()
		self.client.post(reverse('films:new'), data)
		
		# 2. Load all the films saved in the DB
		films = Film.objects.all()
		
		# 3. Now we can compare if the first (and unique) element of the DB list
		#	 has the same name of the data we sended
		self.assertEqual(data['title'], films[0].title)

	def test_create_a_film_with_a_title_and_a_year(self):
		"""
		Send a post to create a film with a title and a year.
		The film is correctly created.
		"""
		# 1. Send the POST with the needed data
		data = self.define_data(year=1999)
		self.client.post(reverse('films:new'), data)
		
		# 2. Load all the films saved in the DB
		films = Film.objects.all()
		
		# 3. Now we can compare if the first (and unique) element of the DB list
		#	 has the same data as we sended
		self.assertEqual(data['title'], films[0].title)
		self.assertEqual(data['year'], films[0].year)

	def test_create_a_film_with_a_title_and_a_description(self):
		"""
		Send a post to create a film with a title and a description.
		The film is correctly created.
		"""
		# 1. Send the POST with the needed data
		data = self.define_data(description='text about the film')
		self.client.post(reverse('films:new'), data)
		
		# 2. Load all the films saved in the DB
		films = Film.objects.all()
		
		# 3. Now we can compare if the first (and unique) element of the DB list
		#	 has the same data as we sended
		self.assertEqual(data['title'], films[0].title)
		self.assertEqual(data['description'], films[0].description)

	def test_create_a_film_with_a_title_a_year_and_a_description(self):
		"""
		Send a post to create a film with a title, a year and a description.
		The film is correctly created.
		"""
		# 1. Send the POST with the needed data
		data = self.define_data(year=1999, description='text about the film')
		self.client.post(reverse('films:new'), data)
		
		# 2. Load all the films saved in the DB
		films = Film.objects.all()
		
		# 3. Now we can compare if the first (and unique) element of the DB list
		#	 has the same data as we sended
		self.assertEqual(data['title'], films[0].title)
		self.assertEqual(data['year'], films[0].year)
		self.assertEqual(data['description'], films[0].description)

	def test_create_a_film_with_a_genre(self):
		"""
		Create a genre. Then send a post to create a film (simple, only a title)
		with that genre.
		"""
		# 1. Create a Genre
		genre = Genre.objects.create(genre_name='terror')
		# 2. Create the correct data, with the Genre, and send de POST
		data = self.define_data(genre=genre.id)
		self.client.post(reverse('films:new'), data)
		# 3. Load all the films saved in the DB
		films = Film.objects.all()
		# 4. Now compare
		self.assertEqual(data['title'], films[0].title)

		self.assertQuerysetEqual(films[0].genre_set.all(), [genre])
		self.assertQuerysetEqual(genre.films.all(), [films[0]])

	def test_create_a_film_and_redirect_to_the_correct_page(self):
		"""
		Create a simple film and the page is redirected to a "detail" view.
		"""
		data = self.define_data()
		response = self.client.post(reverse('films:new'), data)

		films = Film.objects.all()

		expected_url = reverse('films:detail', args=(films[0].id,))

		self.assertRedirects(response, expected_url)


class EditFilmViewTests(TestCase):
	def create_a_film_only_title(self):
		film = Film.objects.create(title='Old title')
		return film

	def create_a_film_full_information(self):
		film = Film.objects.create(title='Old title', year=1999, description='old description')
		return film

	def define_data(self, film, **kwargs):
		data = {
			'call-to': 'edit',
			'id': film.id,
			'title': film.title,
			'year': film.year,
			'description': film.description,
			'watched': film.watched,
		}

		for i in data:
			if data[i] == None:
				data[i] = ''

		for i in kwargs:
			data[i] = kwargs[i]

		return data

	def test_edit_a_title_of_a_film(self):
		"""
		Edit the title of a film, but in two different cases:
		On a hand a film with only a title, on the other hand a film with full information.
		"""
		# 1. A film with only a title:
		film = self.create_a_film_only_title()
		new_title = 'New title'
		self.assertNotEqual(film.title, new_title)
		data = self.define_data(film, title=new_title)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.title, new_title)

		# 2. A film with full information:
			# First empty the DB
		film.delete()
		film = self.create_a_film_full_information()
		self.assertNotEqual(film.title, new_title)
		data = self.define_data(film, title=new_title)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.title, new_title)

	def test_edit_a_year_of_a_film(self):
		"""
		Edit the year of a film, but in two different cases:
		On a hand a film with only a title, on the other hand a film with full information.
		"""
		# 1. A film with only a title:
		film = self.create_a_film_only_title()
		new_year = 2020
		self.assertNotEqual(film.year, new_year)
		data = self.define_data(film, year=new_year)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.year, new_year)

		# 2. A film with full information:
			# First empty the DB
		film.delete()
		film = self.create_a_film_full_information()
		self.assertNotEqual(film.year, new_year)
		data = self.define_data(film, year=new_year)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.year, new_year)

	def test_edit_a_description_of_a_film(self):
		"""
		Edit the description of a film, but in two different cases:
		On a hand a film with only a title, on the other hand a film with full information.
		"""
		# 1. A film with only a title:
		film = self.create_a_film_only_title()
		new_description = 'New description'
		self.assertNotEqual(film.description, new_description)
		data = self.define_data(film, description=new_description)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.description, new_description)

		# 2. A film with full information:
			# First empty the DB
		film.delete()
		film = self.create_a_film_full_information()
		self.assertNotEqual(film.description, new_description)
		data = self.define_data(film, description=new_description)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.description, new_description)

	def test_edit_a_watched_of_a_film(self):
		"""
		Edit the watched of a film, but in two different cases:
		On a hand a film with only a title, on the other hand a film with full information.
		"""
		# 1. A film with only a title:
		film = self.create_a_film_only_title()
		new_watched = True
		self.assertNotEqual(film.watched, new_watched)
		data = self.define_data(film, watched=new_watched)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.watched, new_watched)

		# 2. A film with full information:
			# First empty the DB
		film.delete()
		film = self.create_a_film_full_information()
		self.assertNotEqual(film.watched, new_watched)
		data = self.define_data(film, watched=new_watched)
		self.client.post(reverse('films:detail', args=(film.id,)), data)
			# Reload the 'film' object from the DB
		film = Film.objects.get(pk=film.id)
		self.assertEqual(film.watched, new_watched)

	def test_edit_a_film_and_redirect_to_the_correct_page(self):
		"""
		Edit a film (not matters what) and the page is redirected to the 'detail' view
		of the same film but with the new information.
		"""
		film = self.create_a_film_only_title()
		data = self.define_data(film, title='New title')
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
		expected_url = reverse('films:detail', args=(film.id,))
		self.assertRedirects(response, expected_url)


class DeleteFilmViewTests(TestCase):
	def test_delete_a_film(self):
		"""
		Create a Film and delete by the view 'delete_film()'.
		"""
		film = Film.objects.create(title='Film to delete')
		data = {
			'call-to': 'delete',
			'id': film.id,
		}
		self.assertQuerysetEqual(Film.objects.all(), [film])
		self.client.post(reverse('films:detail', args=(film.id,)), data)
		self.assertQuerysetEqual(Film.objects.all(), [])

	def test_delete_a_film_and_redirect_to_the_correct_page(self):
		"""
		Create and delete a Film and the page is redirected to the main page('mylist')
		"""
		film = Film.objects.create(title='Film to delete')
		data = {
			'call-to': 'delete',
			'id': film.id,
		}
		self.assertQuerysetEqual(Film.objects.all(), [film])
		response = self.client.post(reverse('films:detail', args=(film.id,)), data)
		self.assertQuerysetEqual(Film.objects.all(), [])

		expected_url = reverse('films:list')
		self.assertRedirects(response, expected_url)