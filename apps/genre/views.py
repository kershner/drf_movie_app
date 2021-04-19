from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.genre.serializers import GenreSerializer
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from django.core.paginator import Paginator
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
        movie_list = Movie.objects.filter(genres__id=self.get_object().id).order_by('-id').all()
        paginator = Paginator(movie_list, 40)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['movie_list'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = True
        return context
