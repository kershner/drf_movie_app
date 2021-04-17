from movie_app.apps.movie_credit.serializers import MovieCreditSerializer
from movie_app.apps.movie.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    cast = MovieCreditSerializer(source='get_cast', many=True)

    class Meta:
        model = Movie
        exclude = ['updated_at']
