from movie_app.apps.movie_credit.models import MovieCredit
from rest_framework import serializers


class MovieCreditSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieCredit
        exclude = ['updated_at']
