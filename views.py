from movie_app.apps.person.models import Person
from movie_app.apps.movie.models import Movie
from django.db.models import Count
from django.shortcuts import render
from movie_app import util


def home(request):
    num_results = 20
    movie_pks = Movie.objects.values_list('id', flat=True)
    recent_movies = Movie.objects.filter(pk__in=util.get_random_pks(pks=movie_pks, limit=len(movie_pks))).all()[:num_results]
    recent_people = Person.objects.filter(tmdb_image_path__isnull=False).annotate(c=Count('moviecredit')).all().order_by('-c')[:num_results]
    ctx = {
        'recent_movies': recent_movies,
        'recent_people': recent_people
    }
    return render(request, 'home/home.html', ctx)
