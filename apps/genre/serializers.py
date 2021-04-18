from movie_app.apps.genre.models import Genre
from rest_framework import serializers


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        exclude = ['updated_at']
