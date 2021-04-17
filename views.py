from movie_app.apps.person.models import Person
from movie_app.apps.movie.models import Movie
from django.shortcuts import render
from movie_app import util


def home(request):
    movie_pks = Movie.objects.values_list('id', flat=True)
    people_pks = Person.objects.values_list('id', flat=True)

    num_results = 20
    recent_movies = Movie.objects.filter(pk__in=util.get_random_pks(pks=movie_pks, limit=len(movie_pks))).all()[:num_results]
    recent_people = Person.objects.filter(pk__in=util.get_random_pks(pks=people_pks, limit=len(people_pks))).all()[:num_results]
    ctx = {
        'recent_movies': recent_movies,
        'recent_people': recent_people
    }
    return render(request, 'home.html', ctx)
