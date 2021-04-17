from django.core.management import BaseCommand
from movie_app.apps.movie.models import Movie
from datetime import datetime
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'
    base_endpoint = 'movie'

    def handle(self, *args, **options):
        # Add some movies
        total_movies_to_request = 48
        tmdb_ids = self.get_popular_movie_ids(num_movies=total_movies_to_request)

        count = 1
        total = len(tmdb_ids)
        for tmdb_id in tmdb_ids:
            print('\nRequesting movie ID: {} - {} of {}...'.format(tmdb_id, count, total))
            count += 1
            endpoint = '{}/{}'.format(self.base_endpoint, tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            movie_json = response.json()
            # print(json.dumps(movie_json, indent=2))
            print(movie_json['original_title'])

            movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id)
            movie.title = movie_json['original_title']
            movie.overview = movie_json['overview']
            movie.runtime = movie_json['runtime']
            movie.budget = movie_json['budget']
            movie.release_date = datetime.strptime(movie_json['release_date'], '%Y-%m-%d')
            movie.tmdb_id = movie_json['id']
            movie.tmdb_image_path = movie_json['poster_path']
            movie.save()

    def get_popular_movie_ids(self, num_movies):
        tmdb_ids = []
        page = 1
        while num_movies > 0:
            endpoint = '{}/popular'.format(self.base_endpoint)
            extra_params = '&page={}'.format(page)
            response = util.tmdb_request(endpoint=endpoint, extra_params=extra_params)
            results = response.json()['results']
            for movie in results:
                if num_movies == 0:
                    break

                if movie['id'] not in tmdb_ids:
                    tmdb_ids.append(movie['id'])
                    num_movies -= 1

            page += 1

        return tmdb_ids
