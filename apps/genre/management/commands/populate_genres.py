from django.core.management import BaseCommand
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'

    def handle(self, *args, **options):
        movies = Movie.objects.order_by('id').all()
        total_movies = len(movies)
        movie_count = 1
        for movie in movies:
            print('- Requesting movie genres for: {} - {} of {}...'.format(movie, movie_count, total_movies))
            movie_count += 1

            # Make request for movie credits
            endpoint = 'movie/{}'.format(movie.tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            genres = response.json()['genres']
            for item in genres:
                genre, created = Genre.objects.get_or_create(tmdb_id=item['id'])
                if created:
                    genre.name = item['name']
                    genre.save()

                movie.genres.add(genre)
