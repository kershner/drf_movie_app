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
        popular_people = Person.objects.order_by('-popularity').all()[:1000]
        total_people = len(popular_people)
        person_count = 1
        for person in popular_people:
            print('- Requesting movie credits for: {} - {} of {}...'.format(person, person_count, total_people))
            person_count += 1

            # Make request for movie credits
            endpoint = 'person/{}/movie_credits'.format(person.tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            cast_list = response.json()['cast']
            for item in cast_list:
                if 'release_date' in item:  # Not pulling unreleased movies
                    movie_tmdb_id = item['id']
                    print('Saving: {} - {}'.format(item['original_title'], item['character']))
                    movie, created = Movie.objects.get_or_create(tmdb_id=movie_tmdb_id)
                    if created:
                        # On Movie create, make extra call to TMDB API to get its details
                        endpoint = 'movie/{}'.format(movie_tmdb_id)
                        print('--- Requesting movie info for: {}...'.format(item['title']))
                        response = util.tmdb_request(endpoint=endpoint)
                        movie_json = response.json()
                        movie.title = movie_json['original_title']
                        movie.overview = movie_json['overview']
                        movie.runtime = movie_json['runtime']
                        movie.budget = movie_json['budget']

                        try:
                            movie.release_date = datetime.strptime(movie_json['release_date'], '%Y-%m-%d')
                        except ValueError as e:
                            print('{} does not match format %Y-%m-%d'.format(movie_json['release_date']))
                        movie.tmdb_image_path = movie_json['poster_path']
                        movie.save()

                    print('-- Saving: {} - {}'.format(person.name, item['character']))
                    movie_credit, created = MovieCredit.objects.get_or_create(person=person, movie=movie)
                    movie_credit.movie_title = movie.title
                    movie_credit.actor_name = person.name
                    movie_credit.release_date = movie.release_date
                    movie_credit.role = item['character']
                    if 'poster_path' in item:
                        movie_credit.tmdb_image_path = item['poster_path']
                    movie_credit.save()

        # # Query for each Movie object's cast
        # movies = Movie.objects.all()
        # total_movies = len(movies)
        # movie_count = 1
        # for movie in movies:
        #     print('- Requesting movie credits for: {} - {} of {}...'.format(movie, movie_count, total_movies))
        #     movie_count += 1
        #
        #     # Make request for movie credits
        #     endpoint = 'movie/{}/credits'.format(movie.tmdb_id)
        #     response = util.tmdb_request(endpoint=endpoint)
        #     cast_list = response.json()['cast']
        #     for item in cast_list:
        #         person_id = item['id']
        #         person, created = Person.objects.get_or_create(tmdb_id=person_id)
        #         if created:
        #             # On Person create, make extra call to TMDB API to get their details
        #             endpoint = 'person/{}'.format(person_id)
        #             print('-- Requesting person info for: {}...'.format(item['name']))
        #             response = util.tmdb_request(endpoint=endpoint)
        #             person_json = response.json()
        #             person.name = person_json['name']
        #             person.bio = person_json['biography']
        #             person.place_of_birth = person_json['place_of_birth']
        #             if person_json['birthday']:
        #                 try:
        #                     person.birthday = datetime.strptime(person_json['birthday'], '%Y-%m-%d')
        #                 except ValueError as e:
        #                     print('{} does not match format %Y-%m-%d'.format(person_json['birthday']))
        #             if person_json['deathday']:
        #                 try:
        #                     person.deathday = datetime.strptime(person_json['deathday'], '%Y-%m-%d')
        #                 except ValueError as e:
        #                     print('{} does not match format %Y-%m-%d'.format(person_json['deathday']))
        #             person.tmdb_image_path = person_json['profile_path']
        #             person.save()
        #
        #         print('-- Saving: {} - {}'.format(item['name'], item['character']))
        #         movie_credit, created = MovieCredit.objects.get_or_create(person=person, movie=movie)
        #         movie_credit.movie_title = movie.title
        #         movie_credit.actor_name = item['name']
        #         movie_credit.release_date = movie.release_date
        #         movie_credit.role = item['character']
        #         if 'poster_path' in item:
        #             movie_credit.tmdb_image_path = item['poster_path']
        #         movie_credit.save()

