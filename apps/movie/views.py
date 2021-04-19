from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.movie.serializers import MovieSerializer
from movie_app.apps.movie.models import Movie
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.views import generic


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movie/movie_list.html'
    paginate_by = 80


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movie/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cast_list = self.get_object().get_cast()
        paginator = Paginator(cast_list, 40)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['cast'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = True
        return context
