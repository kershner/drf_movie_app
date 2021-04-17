from movie_app.apps.movie.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        exclude = ['updated_at']
