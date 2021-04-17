from movie_app.apps.movie_credit.serializers import MovieCreditSerializer
from movie_app.apps.person.models import Person
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    movie_credits = MovieCreditSerializer(many=True, source='get_movie_credits')

    class Meta:
        model = Person
        exclude = ['updated_at']
