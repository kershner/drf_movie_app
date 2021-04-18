from django.core.management import BaseCommand
from movie_app.apps.person.models import Person
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'
    base_endpoint = 'person'

    def handle(self, *args, **options):
        # Add some people
        all_people_without_populariy = Person.objects.filter(popularity__isnull=True).all()
        count = 1
        total = len(all_people_without_populariy)

        for person in all_people_without_populariy:
            print('- [{} of {}] Requesting popularity value for: {}...'.format(count, total, person))
            count += 1
            endpoint = '{}/{}'.format(self.base_endpoint, person.tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            person_json = response.json()
            popularity = person_json['popularity']
            person.popularity = popularity
            person.save()
