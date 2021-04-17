from movie_app.apps.movie_credit.models import MovieCredit
from movie_app.apps.person.models import Person
from django.core.management import BaseCommand
from movie_app.apps.movie.models import Movie
from datetime import datetime
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'

    def handle(self, *args, **options):
        # Add some movies
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
                    movie_credit.movie_title = item['original_title']
                    if 'release_date' in item:
                        try:
                            movie_credit.release_date = datetime.strptime(item['release_date'], '%Y-%m-%d')
                        except ValueError as e:
                            print('{} does not match format: %Y-%m-%d'.format(item['release_date']))
                    movie_credit.role = item['character']
                    movie_credit.tmdb_image_path = item['poster_path']
                    movie_credit.save()
