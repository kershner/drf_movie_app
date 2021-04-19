from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.genre.serializers import GenreSerializer
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from rest_framework import viewsets
from django.views import generic


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GenreDetailView(generic.DetailView):
    model = Genre
    template_name = 'genre/genre_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.filter(genres__id=self.get_object().id).order_by('-id').all()
        return context
