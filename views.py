from movie_app.apps.movie.models import MovieCredit
from movie_app.apps.person.models import Person
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from movie_app.forms import SearchForm
from django.db.models import Count
from django.shortcuts import render
from movie_app import util
import random


def home(request):
    num_results = 20
    movie_pks = Movie.objects.values_list('pk', flat=True)
    popular_movies = Movie.objects.filter(id__in=util.get_random_pks(pks=movie_pks,
                                                                    limit=len(movie_pks))).all()[:num_results]
    people_pks = Person.objects.values_list('pk', flat=True)
    random_people_pks = [random.choice(people_pks) for num in range(num_results)]
    popular_people = Person.objects.filter(tmdb_image_path__isnull=False).filter(id__in=random_people_pks).all().order_by('-popularity')

    character_pks = MovieCredit.objects.values_list('pk', flat=True)
    random_character_pks = [random.choice(character_pks) for num in range(num_results)]
    popular_characters = MovieCredit.objects.filter(pk__in=random_character_pks).all().order_by('-person__popularity')

    genres = Genre.objects.all()

    ctx = {
        'form': SearchForm(),
        'popular_movies': popular_movies,
        'popular_people': popular_people,
        'popular_characters': popular_characters,
        'genres': genres
    }
    return render(request, 'home/home.html', ctx)


def search_results(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            movie_results = Movie.objects.filter(title__icontains=q).annotate(c=Count('moviecredit')).order_by('-c').all()
            person_results = Person.objects.filter(name__icontains=q).order_by('-popularity').all()
            character_results = MovieCredit.objects.filter(role__icontains=q).order_by('-person__popularity').all()
            ctx = {
                'form': form,
                'q': q,
                'movie_results': movie_results,
                'person_results': person_results,
                'character_results': character_results
            }
            return render(request, 'home/search_results.html', ctx)

    return render(request, 'home/search_results.html')
