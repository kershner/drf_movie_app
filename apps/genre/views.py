from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.genre.serializers import GenreSerializer
from movie_app.apps.genre.models import Genre
from rest_framework import viewsets
from django.views import generic


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GenreListView(generic.ListView):
    model = Genre
    template_name = 'genre/genre_list.html'
    paginate_by = 80


class GenreDetailView(generic.DetailView):
    model = Genre
    template_name = 'movie/genre_detail.html'
