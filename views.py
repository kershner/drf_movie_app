from movie_app.apps.movie.models import MovieCredit
from movie_app.apps.person.models import Person
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from movie_app.forms import SearchForm
from django.db.models import Count
from django.shortcuts import render
from movie_app import util


def home(request):
    num_results = 20
    movie_pks = Movie.objects.values_list('id', flat=True)
    recent_movies = Movie.objects.filter(pk__in=util.get_random_pks(pks=movie_pks, limit=len(movie_pks))).all()[:num_results]
    recent_people = Person.objects.filter(tmdb_image_path__isnull=False).annotate(c=Count('moviecredit')).all().order_by('-c')[:num_results]
    genres = Genre.objects.all()
    ctx = {
        'form': SearchForm(),
        'recent_movies': recent_movies,
        'recent_people': recent_people,
        'genres': genres
    }
    return render(request, 'home/home.html', ctx)


def search_results(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            movie_results = Movie.objects.filter(title__icontains=q).annotate(c=Count('moviecredit')).order_by('-c').all()
            person_results = Person.objects.filter(name__icontains=q).annotate(c=Count('moviecredit')).order_by('-c').all()
            character_results = MovieCredit.objects.filter(role__icontains=q).order_by('-created_at').all()
            ctx = {
                'form': form,
                'q': q,
                'movie_results': movie_results,
                'person_results': person_results,
                'character_results': character_results
            }
            return render(request, 'home/search_results.html', ctx)

    return render(request, 'home/search_results.html')
