from movie_app.apps.movie_credit.models import MovieCredit
from movie_app.apps.person.models import Person
from django.core.management import BaseCommand
from movie_app.apps.movie.models import Movie
from datetime import datetime
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'

    def handle(self, *args, **options):
        # Query for each Person object's credits
        people = Person.objects.all()
        total_people = len(people)
        person_count = 1
        for person in people:
            print('Requesting movie credits for: {} - {} of {}...'.format(person, person_count, total_people))
            person_count += 1

            # Make request for movie credits
            endpoint = 'person/{}/movie_credits'.format(person.tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            cast_list = response.json()['cast']
            for item in cast_list:
                if 'release_date' in item:  # Not pulling unreleased movies
                    print('Saving: {} - {}'.format(item['original_title'], item['character']))
                    existing_movie = Movie.objects.filter(title=item['original_title']).first()
                    movie_credit, created = MovieCredit.objects.get_or_create(tmdb_id=item['id'])
                    movie_credit.movie = existing_movie
                    movie_credit.person = person
                    movie_credit.actor_name = person.name
                    movie_credit.movie_title = item['original_title']
                    if 'release_date' in item:
                        try:
                            movie_credit.release_date = datetime.strptime(item['release_date'], '%Y-%m-%d')
                        except ValueError as e:
                            print('{} does not match format: %Y-%m-%d'.format(item['release_date']))
                    movie_credit.role = item['character']
                    movie_credit.tmdb_image_path = item['poster_path']
                    movie_credit.save()

        # Query for each Movie object's cast
        movies = Movie.objects.all()
        total_movies = len(movies)
        movie_count = 1
        for movie in movies:
            print('Requesting movie credits for: {} - {} of {}...'.format(movie, movie_count, total_movies))
            movie_count += 1

            # Make request for movie credits
            endpoint = 'movie/{}/credits'.format(movie.tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            cast_list = response.json()['cast']
            for item in cast_list:
                print('Saving: {} - {}'.format(item['name'], item['character']))
                existing_person = Person.objects.filter(name=item['name']).first()
                movie_credit, created = MovieCredit.objects.get_or_create(tmdb_id=item['id'])
                movie_credit.movie = movie
                movie_credit.person = existing_person
                movie_credit.movie_title = movie.title
                movie_credit.actor_name = item['name']
                movie_credit.release_date = movie.release_date
                movie_credit.role = item['character']
                if 'poster_path' in item:
                    movie_credit.tmdb_image_path = item['poster_path']
                movie_credit.save()

