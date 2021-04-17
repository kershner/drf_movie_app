from django.core.management import BaseCommand
from movie_app.apps.person.models import Person
from datetime import datetime
from movie_app import util


class Command(BaseCommand):
    help = 'Pulls data from TMDB and inserts into DB'
    base_endpoint = 'person'

    def handle(self, *args, **options):
        # Add some people
        total_people_to_request = 1000
        tmdb_ids = self.get_popular_person_ids(num_persons=total_people_to_request)
        count = 1
        total = len(tmdb_ids)

        for tmdb_id in tmdb_ids:
            print('Requesting person ID: {} - {} of {}...'.format(tmdb_id, count, total))
            count += 1
            endpoint = '{}/{}'.format(self.base_endpoint, tmdb_id)
            response = util.tmdb_request(endpoint=endpoint)
            person_json = response.json()
            person, created = Person.objects.get_or_create(tmdb_id=tmdb_id)
            person.name = person_json['name']
            person.bio = person_json['biography']
            person.place_of_birth = person_json['place_of_birth']
            if person_json['birthday']:
                try:
                    person.birthday = datetime.strptime(person_json['birthday'], '%Y-%m-%d')
                except ValueError as e:
                    print('{} does not match format %Y-%m-%d'.format(person_json['birthday']))
            if person_json['deathday']:
                try:
                    person.deathday = datetime.strptime(person_json['deathday'], '%Y-%m-%d')
                except ValueError as e:
                    print('{} does not match format %Y-%m-%d'.format(person_json['deathday']))
            person.tmdb_id = person_json['id']
            person.tmdb_image_path = person_json['profile_path']
            person.save()

    def get_popular_person_ids(self, num_persons):
        tmdb_ids = []
        page = 1
        while num_persons > 0:
            endpoint = '{}/popular'.format(self.base_endpoint)
            extra_params = '&page={}'.format(page)
            response = util.tmdb_request(endpoint=endpoint, extra_params=extra_params)
            results = response.json()['results']
            for person in results:
                if num_persons == 0:
                    break

                if person['id'] not in tmdb_ids:
                    tmdb_ids.append(person['id'])
                    num_persons -= 1

            page += 1

        return tmdb_ids
