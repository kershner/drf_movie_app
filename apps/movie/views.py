from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.movie.serializers import MovieSerializer
from movie_app.apps.movie.models import Movie
from rest_framework import viewsets


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
