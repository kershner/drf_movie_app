from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.movie.serializers import MovieSerializer
from movie_app.apps.movie.models import Movie
from rest_framework import viewsets
from django.views import generic


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movie/movie_list.html'
    paginate_by = 40


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movie/movie_detail.html'
